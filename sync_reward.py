"""

本进程负责以下工作

+ 统计 RNode 历史 Reward 奖励
+ 统计 RNode 历史按天出块数、按天奖励
+ 监控 RNode 状态
    + running: 1小时内有发送到 Campaign 合约的交易

sudo docker run -it --name sync_reward -v `pwd`:/cpchain-website liaojl/website python sync_reward.py

"""

import time
from log import get_log
from datetime import datetime
from tools.dingding import post_message
from apps.chain.db import cpchain_db, block_collection

logger = get_log('sync-reward')


RNODE_REWARD_META = 'rnode_reward_meta'
RNODE_REWARD_TOTEL = 'rnode_reward_total'
RNODE_REWARD_HISTORY = 'rnode_reward_history'


def get_meta(col):
    if col.count_documents({}) == 0:
        col.insert({
            'current_block': 0
        })
        return 0
    return col.find()[0]['current_block']


def update_meta(col, current):
    col.update_one({'current_block': {'$exists': True}},  {
                   "$set": {'current_block': current}}, True)


def get_latest(col):
    return col.find({}).sort('_id', -1).limit(1)[0]['number']

def is_date_equal(t1, t2):
    return t1.strftime('%Y-%m-%d') == t2.strftime('%Y-%m-%d')

def update_rewards(c_total, c_history, miner, reward, timestamp):
    old_reward = 0
    old_timestamp = timestamp
    ttb = 0 # total blocks
    tb = 0 # today blocks
    tr = 0 # today rewards
    if c_total.count_documents({'miner': miner}) == 0:
        c_total.insert({
            'miner': miner,
            'reward': old_reward,
            'timestamp': old_timestamp,
            'total_blocks': 0,
            'today_blocks': 0,
            'today_reward': 0
        })
    else:
        r = c_total.find({'miner': miner})[0]
        old_reward = r['reward']
        old_timestamp = r['timestamp']
        ttb = r['total_blocks']
        tb = r['today_blocks']
        tr = r['today_reward']
    
    # 判断是否为今天
    if is_date_equal(old_timestamp, timestamp):
        tb += 1
        tr += reward
    else:
        # 插入历史记录
        c_history.insert({
            'miner': miner,
            'blocks': tb,
            'rewards': tr,
            'date': datetime.strptime(timestamp.strftime('%Y-%m-%d'), '%Y-%m-%d')
        })
        # 今日清零
        tb = 1
        tr = reward

    ttb += 1
    reward += old_reward
    c_total.update_one({'miner': miner},  {
        "$set": {
            'reward': reward,
            'timestamp': timestamp,
            'total_blocks': ttb,
            'today_blocks': tb,
            'today_reward': tr
        }
    }, True)


def sync_rnode_rewards(c_blocks):
    try:
        c_meta = cpchain_db[RNODE_REWARD_META]
        c_total = cpchain_db[RNODE_REWARD_TOTEL]
        c_history = cpchain_db[RNODE_REWARD_HISTORY]

        # 获取最近遍历的区块号
        current = get_meta(c_meta)

        while True:
            if current < get_latest(c_blocks):
                current += 1
                logger.info("sync block #%d", current)
                b = c_blocks.find({'number': current})[0]
                miner = b['miner']
                reward = float(b['reward'])
                timestamp = datetime.fromtimestamp(b['timestamp'])
                if reward > 0:
                    # 总收益、每日出块数、每日收益
                    update_rewards(c_total, c_history, miner, reward, timestamp)
                update_meta(c_meta, current)
            else:
                time.sleep(10)
    except Exception as e:
        logger.error(e)
        post_message(f"**sync reward error:**\n{e}")

if __name__ == '__main__':
    sync_rnode_rewards(block_collection)
