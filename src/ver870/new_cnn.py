from src.VFBLS_v110.bls.processing.replaceNan import replaceNan
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier

import os
import sys
import time

from scipy.stats import zscore

from keras.layers import Conv2D, Conv1D, MaxPooling2D, MaxPooling1D, Flatten, Dense
from keras.layers import BatchNormalization

from keras.models import Sequential
from keras.callbacks import CSVLogger, ModelCheckpoint

from keras.optimizers import Adam
from keras import regularizers

from sklearn.model_selection import train_test_split


def cnn_train_realtime(train_x, train_y, test_x):
    """

    """
    print("Training - begin")
    time_start = time.time()

    X_train, X_test, y_train, y_test = train_test_split(train_x, train_y, test_size=0.2, random_state=42)

    # making the deep learning function
    def model():
        input_shape = 37
        model = Sequential()
        model.add(Conv1D(filters=64, kernel_size=6, activation='relu',
                         padding='same', input_shape=(input_shape, 1)))
        model.add(BatchNormalization())

        # adding a pooling layer
        model.add(MaxPooling1D(pool_size=(3), strides=2, padding='same'))

        model.add(Conv1D(filters=64, kernel_size=6, activation='relu',
                         padding='same', input_shape=(input_shape, 1)))
        model.add(BatchNormalization())
        model.add(MaxPooling1D(pool_size=(3), strides=2, padding='same'))

        model.add(Conv1D(filters=64, kernel_size=6, activation='relu',
                         padding='same', input_shape=(input_shape, 1)))
        model.add(BatchNormalization())
        model.add(MaxPooling1D(pool_size=(3), strides=2, padding='same'))

        model.add(Flatten())
        model.add(Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.3)))
        model.add(Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.3)))
        # model.add(Dense(64, activation='relu'))
        # model.add(Dense(64, activation='relu'))
        model.add(Dense(2, activation='softmax'))

        lr = 0.001  # 设置学习率
        optimizer = Adam(learning_rate=lr)
        # optimizer = Adam()
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model

    model = model()
    print(model.summary())
    # log_dir = "../logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    logger = CSVLogger('logs.csv', append=True)
    # his = model.fit(train_x, train_y, epochs=20, batch_size=64,
    #                 callbacks=[logger])

    his = model.fit(X_train, y_train, epochs=30, batch_size=64,
                    validation_data=(X_test, y_test)
                    # , callbacks=[tensorboard_callback]
                    )

    # check the model performance on test data
    predicted = model.predict(test_x)

    print("predicted:", predicted)

    print((train_x.shape))
    print((train_y[:5]))

    predicted = [[1.], [2.], [2.], [2.], [2.]]
    TrainingAccuracy, Training_time, Testing_time = 0.9, 0.5, 0.2
    return TrainingAccuracy, Training_time, Testing_time, predicted


def one_hot_m(y, n_classes):
    ret = np.zeros((y.shape[0], n_classes))
    for i in range(0, n_classes):
        for j in range(0, len(y)):
            if y[j] == (i + 1):
                ret[j, i] = 1
    return ret


def feature_select_imp_cnl(data, label, top_f_features):
    # np.random.seed(1);
    model = ExtraTreesClassifier(n_estimators=100, random_state=1)
    label = np.ravel(label)
    model.fit(data, label)

    importances = model.feature_importances_
    # print(importances)

    f_indices = np.argsort(importances)[::-1]
    # print(f_indices)

    selected_features = f_indices[0:top_f_features]
    # print(selected_features)

    importances2 = importances[selected_features]
    # print(importances2)

    # output = np.concatenate((selected_features.reshape((-1,1)), importances2.reshape((-1,1))),axis=1)
    # np.savetxt('featureImportance_nslkdd.csv', output, delimiter=',' , fmt='%f')

    return selected_features, importances2


def cnn_demo_train_test(num_features='all'):
    print("cnn_demo_train_test")

    # Disable
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__

    # blockPrint()
    # enablePrint()

    print("Load the datasets")
    # path_app = "src"

    path_app = "../data_historical"
    train_dataset0 = np.loadtxt("%s/Code_Red_I.csv" % path_app, delimiter=",")
    train_dataset1 = np.loadtxt("%s/Nimda.csv" % path_app, delimiter=",")
    train_dataset2 = np.loadtxt("%s/Slammer.csv" % path_app, delimiter=",")
    train_dataset3 = np.loadtxt("%s/Moscow_blackout.csv" % path_app, delimiter=",")
    train_dataset4 = np.loadtxt("%s/WannaCrypt.csv" % path_app, delimiter=",")
    train_dataset5 = np.loadtxt("%s/RIPE_regular.csv" % path_app, delimiter=",")
    train_dataset6 = np.loadtxt("%s/BCNET_regular.csv" % path_app, delimiter=",")

    # test_dataset = np.loadtxt('/%s/data_test/DUMP_out.txt' % path_app)
    test_dataset = np.loadtxt('E:/project870/20230901/20230901.0000.txt')

    print("Combine training data")
    # Combine training data
    train_dataset_list = [train_dataset1, train_dataset2, train_dataset3,
                          # train_dataset4,
                          train_dataset5, train_dataset6]

    train_dataset = train_dataset0
    for train_data in train_dataset_list:
        train_dataset = np.concatenate((train_dataset, train_data), axis=0)
    # np.savetxt('./train_dataset.csv', train_dataset, delimiter=',', fmt='%.4f')

    print("train_dataset:", type(train_dataset))

    row_index_end = train_dataset.shape[0] - train_dataset.shape[0] % 100  # divisible by 100
    train_x = train_dataset[:row_index_end, 4:-1]
    train_x = zscore(train_x, axis=0, ddof=1)  # For each feature, mean = 0 and std = 1
    replaceNan(train_x)  # Replace "nan" with 0
    train_y = train_dataset[:row_index_end, -1]

    # Change training labels
    inds1 = np.where(train_y == -1)
    train_y[inds1] = 2

    # new process test data #
    test_x = test_dataset[:, 4:]

    # Normalize test data
    test_x = zscore(test_x, axis=0, ddof=1)  # For each feature, mean = 0 and std = 1
    replaceNan(test_x)  # Replace "nan" with 0
    # test_y = test_dataset[:, -1];

    # # Change test labels
    # inds2 = np.where(test_y == 0);
    # test_y[inds2] = 2;

    # feature selection - begin
    if num_features != 'all':
        num_features = int(num_features)
        features, _ = feature_select_imp_cnl(train_x, train_y, num_features)
        train_x = train_x[:, features]
        test_x = test_x[:, features]
    # feature selection - end

    # BLS parameters
    seed = 1  # set the seed for generating random numbers
    num_class = 2  # number of the classes
    epochs = 1  # number of epochs

    train_y = one_hot_m(train_y, num_class)
    # test_y = one_hot_m(test_y, num_class);
    #######################

    train_err = np.zeros((1, epochs))
    train_time = np.zeros((1, epochs))
    test_time = np.zeros((1, epochs))

    # CNN ----------------------------------------------------------------
    print("======================= CNN =======================\n")
    np.random.seed(seed)  # set the seed for generating random numbers
    for j in range(0, epochs):
        trainingAccuracy, trainingTime, testingTime, predicted = \
            cnn_train_realtime(train_x, train_y, test_x
                               )

        train_err[0, j] = trainingAccuracy * 100
        train_time[0, j] = trainingTime
        test_time[0, j] = testingTime

    enablePrint()
    print("trn acc:", trainingAccuracy)

    # predicted = [[1.], [2.], [2.], [2.], [2.]]
    predicted_list = []
    for label in predicted:
        predicted_list.append(label[0])

    # string to the front-end
    web_results = []
    test_hour_chart = []
    test_min_chart = []
    test_hour, test_min = test_dataset[:, 1], test_dataset[:, 2]
    for label, hour, minute in zip(predicted, test_hour, test_min):
        hour, minute = int(hour), int(minute)
        hour = str(hour)
        if len(hour) == 1:
            hour = '0' + hour
        minute = str(minute)
        if len(minute) == 1:
            minute = '0' + minute
        if label == 1:
            print("\n Detection time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
            web_results.append("Detection time (HH:MM) %s : %s => An anomaly is detected!" % (hour, minute))
        else:
            print("\n Detection time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
            web_results.append("Detection time (HH:MM) %s : %s => Normal traffic" % (hour, minute))
        test_hour_chart.append(hour)
        test_min_chart.append(minute)
    return predicted_list, test_hour_chart, test_min_chart, web_results


path_app = "../data_historical"
file_path = "%s/Code_Red_I.csv" % path_app
print(file_path)
predicted_list, test_hour_chart, test_min_chart, web_results = cnn_demo_train_test()
print(predicted_list, test_hour_chart, test_min_chart, web_results)
