#变量初始化区域
pair_list=[]
low_list = []
high_list = []

#取数据区域
for i in range(0, total):
    today_high=get("最高价", i)
    today_low=get("最低价", i)
    pair_list.append((today_low, today_high))
    low_list.append(today_low)
    high_list.append(today_high)

#计算数据区域
def check_merge_pairs_helper(pair1, pair2, upward):
    if upward:
        return pair1[0] < pair2[0] and pair1[1] > pair2[1]
    else:
        return pair1[0] > pair2[0] and pair1[1] < pair2[1]

def check_merge_pairs(pair1, pair2, upward):
    return check_merge_pairs_helper(pair1, pair2, upward) or check_merge_pairs_helper(pair2, pair1, upward)

def merge_pairs(pair1, pair2, upward):
    if upward:
        return (max(pair1[0], pair2[0]), max(pair1[1], pair2[1]))
    else:
        return (min(pair1[0], pair2[0]), min(pair1[1], pair2[1]))

def check_revert_trend(current_pair, next_pair_idx, trend_count, increment_idx, upward, value_to_compare):
    if next_pair_idx < 0 or next_pair_idx >= len(pair_list):
        return False
    if trend_count >= 1:
        return True
    if upward and current_pair[0] > value_to_compare: 
        return False
    if not upward and current_pair[1] < value_to_compare: 
        return False
    if check_merge_pairs(current_pair, pair_list[next_pair_idx], upward):
        pair_to_check = merge_pairs(current_pair, pair_list[next_pair_idx], upward)
        if increment_idx:
            next_pair_idx += 1
        else:
            next_pair_idx += -1
    else:
        pair_to_check = pair_list[next_pair_idx]
        trend_count += 1
    if increment_idx:
        return check_revert_trend(pair_to_check, next_pair_idx + 1, trend_count, increment_idx, upward, value_to_compare)
    else:
        return check_revert_trend(pair_to_check, next_pair_idx - 1, trend_count, increment_idx, upward, value_to_compare)

def get_turning_points(pairs, lows, highs):
    min_val = min(lows)
    max_val = max(highs)
    min_idx = lows.index(min_val)
    max_idx = highs.index(max_val)
    
    result = []
    result.append((max_idx, max_val))
    
    upward_trend = False
    compare_val = max_val
    for i in range(max_idx, len(pairs)):
        if (check_revert_trend(pairs[i], i + 1, 0, True, upward_trend, compare_val)):
            if upward_trend:
                result.append((i, pairs[i][1]))
                # save("转折点", pairs[i][1], i)
                compare_val = pairs[i][1]
            else:
                result.append((i, pairs[i][0]))
                # save("转折点", pairs[i][0], i)
                compare_val = pairs[i][0]
            upward_trend = not upward_trend
    
    upward_trend = False
    compare_val = max_val
    for i in range(max_idx, -1, -1):
        if (check_revert_trend(pairs[i], i - 1, 0, False, upward_trend, compare_val)):
            if upward_trend:
                result.append((i, pairs[i][1]))
                # save("转折点", pairs[i][1], i)
                compare_val = pairs[i][1]
            else:
                result.append((i, pairs[i][0]))
                # save("转折点", pairs[i][0], i)
                compare_val = pairs[i][0]
            upward_trend = not upward_trend
            
    return result
            

turning_points = get_turning_points(pair_list, low_list, high_list)
sorted_turning_points = sorted(turning_points, key=lambda v: v[0])
#画线区域
for pt in sorted_turning_points:
    save("转折点", pt[1], pt[0])
draw.curve("转折点")
