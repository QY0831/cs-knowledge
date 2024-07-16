# 每个位置i可向后跳跃（覆盖）到位置j，从i=0出发，求到达指定位置的最小步数

# https://leetcode.cn/problems/jump-game-ii/
# 45. 跳跃游戏 II
class Solution:
    def jump(self, nums: List[int]) -> int:
        max_pos = 0 # next step max position
        end = 0 # current step max position
        step = 0
        for i in range(len(nums) - 1):
            if i <= end:
                max_pos = max(max_pos, i + nums[i])
                if i == end: # have to jump
                    step += 1
                    end = max_pos
        return step
    
    
# https://leetcode.cn/problems/video-stitching/description/
# 1024. 视频拼接
class Solution:
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        mx = [0] * time
        for l, r in clips:
            if l < time:
                mx[l] = max(mx[l], r)

        max_pos = 0 # next step max position
        end = 0 # current step max position
        step = 0

        for i in range(time):
            if i > end:
                return -1
            max_pos = max(max_pos, mx[i])
            if i == end:
                step += 1
                end = max_pos
        if end >= time:
            return step
        return -1
    
    
# https://leetcode-cn.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/
# 1326. 灌溉花园的最少水龙头数目
class Solution:
    def minTaps(self, n: int, ranges: List[int]) -> int:
        mx = [0] * (n + 1)
        for i, r in enumerate(ranges):
            left = max(0, i - r)
            mx[left] = max(mx[left], i + r)
        
        max_pos = end = step = 0
        for i in range(n + 1):
            if i > end:
                return -1
            if i == n:
                return step
            max_pos = max(max_pos, mx[i])
            if i == end:
                step += 1
                end = max_pos
        return step
