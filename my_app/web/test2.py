



from multiprocessing import cpu_count, Pool

# cpu 数量
cores = cpu_count()
print('cores数量',cores)
# 分块个数
partitions = cores


def parallelize(data_split,func):
    """
    多核并行处理模块
    :param df: DataFrame数据
    :param func: 预处理函数
    :return: 处理后的数据
    """
    # 数据切分
    # data_split = np.array_split(df, partitions)
    # 线程池
    pool = Pool(2)
    # 数据分发 合并
    data = pool.map(func, data_split)
    # 关闭线程池
    pool.close()
    # 执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    pool.join()
    return data

















