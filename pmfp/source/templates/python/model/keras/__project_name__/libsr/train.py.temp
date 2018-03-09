from keras.optimizers import SGD


def train(model_blueprint, x, y, epochs, batch_size,
          optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True),
          loss='categorical_crossentropy',
          metrics=['accuracy'], **kwargs):
    """用训练集和标签集训练模型

    Parameters:
        model_blueprint (Keras_model): - 训练前搭建好的模型结构
        x (np.ndarray): - 用于训练的特征集
        y (np.ndarray): - 用于训练的标签集
        epochs (int): - 训练多少次样本,1个epoch等于使用训练集中的全部样本训练一次
        batch_size (int): - 批大小.每次训练在训练集中取batchsize个样本训练
        optimizer (keras.optimizers): - 定义好的优化方式
        loss (str): - 指定好的损失函数
        metrics (list[str]): - 指明度量标准
        kwargs (dict[str,any]): - fit方法使用的参数

    Returns:
        Keras_model: - 训练完后的模型对象
    """
    model_blueprint.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    print(model_blueprint.summary())
    model_blueprint.fit(x, y, epochs=epochs, batch_size=batch_size, **kwargs)
    return model_blueprint


def train_generator(model_blueprint, generator, steps_per_epoch, epochs=1,
                    optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True),
                    loss='categorical_crossentropy',
                    metrics=['accuracy'], **kwargs):
    """用训练数据生成器训练模型,使用的生成器是不会终止的.且yield出来的数据是[X,y]的形式

    Parameters:
        model_blueprint (Keras_model): - 训练前搭建好的模型结构
        generator (generator): - 每次可以yield出一批待训练数据的生成器
        steps_per_epoch (int): - 每个epochs训练多少个generator的next后得到的数据
        epochs (int): - 训练多少次样本,1个epoch等于使用训练集中的全部样本训练一次
        optimizer (keras.optimizers): - 定义好的优化方式
        loss (str): - 指定好的损失函数
        metrics (list[str]): - 指明度量标准
        kwargs (dict[str,any]): - fit方法使用的参数

    Returns:
        Keras_model: - 训练完后的模型对象
    """
    model_blueprint.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    print(model_blueprint.summary())
    model_blueprint.fit_generator(generator,
                                  steps_per_epoch,
                                  epochs=epochs,
                                  **kwargs)
    return model_blueprint
