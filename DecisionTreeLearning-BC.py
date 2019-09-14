import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn import tree
from sklearn.model_selection import learning_curve
from matplotlib.ticker import MaxNLocator
from sklearn.model_selection import validation_curve
from sklearn.model_selection import GridSearchCV

class decisionTreeLearner():
    def __init__(self, pathToData):
        self.dataFilePath = pathToData

    def plotBCDataCharacteristics(self):
        for col in self.df.columns:
            if col=='Class':
                break
            x1 = self.df.loc[self.df.Class==2, col]
            x2 = self.df.loc[self.df.Class==4, col]
            bins = np.linspace(0, 10, 20)
            plt.hist(x1, bins, alpha=0.5, label='Benign')
            plt.hist(x2, bins, alpha=0.5, label='Malignant')
            plt.legend(loc='upper right')
            plt.xlabel(col)
            plt.ylabel('Sample counts')
            filename = '{}/images/{}_{}_{}_dist.png'.format('.', 'DT', 'BC',col)
            plt.savefig(filename, format='png', dpi=150)
            plt.close()

    def loadBCData(self):
        self.df = pd.read_csv(self.dataFilePath, header=1, index_col=0)

    def plot_confusion_matrix(self,y_true, y_pred, classes,
                              normalize=False,
                              title=None,
                              cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """
        if not title:
            if normalize:
                title = 'Normalized confusion matrix'
            else:
                title = 'Confusion matrix, without normalization'

        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        # Only use the labels that appear in the data
        classes = classes[unique_labels(y_true, y_pred)]
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        print(cm)

        fig, ax = plt.subplots()
        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        ax.figure.colorbar(im, ax=ax)
        # We want to show all ticks...
        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               # ... and label them with the respective list entries
               xticklabels=classes, yticklabels=classes,
               title=title,
               ylabel='True label',
               xlabel='Predicted label')

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center")
        fig.tight_layout()
        return ax

    # Code utilized from Scikit learn.
    def plot_learning_curve(self,estimator, title, X, y, ylim=None, cv=None,
                            n_jobs=None, train_sizes=np.append(np.linspace(0.05, 0.1, 10, endpoint=False),
                                                               np.linspace(0.1, 1, 10, endpoint=True))):
        """
        Generate a simple plot of the test and training learning curve.

        Parameters
        ----------
        estimator : object type that implements the "fit" and "predict" methods
            An object of that type which is cloned for each validation.

        title : string
            Title for the chart.

        X : array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape (n_samples) or (n_samples, n_features), optional
            Target relative to X for classification or regression;
            None for unsupervised learning.

        ylim : tuple, shape (ymin, ymax), optional
            Defines minimum and maximum yvalues plotted.

        cv : int, cross-validation generator or an iterable, optional
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:
              - None, to use the default 3-fold cross-validation,
              - integer, to specify the number of folds.
              - :term:`CV splitter`,
              - An iterable yielding (train, test) splits as arrays of indices.

            For integer/None inputs, if ``y`` is binary or multiclass,
            :class:`StratifiedKFold` used. If the estimator is not a classifier
            or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

            Refer :ref:`User Guide <cross_validation>` for the various
            cross-validators that can be used here.

        n_jobs : int or None, optional (default=None)
            Number of jobs to run in parallel.
            ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
            ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
            for more details.

        train_sizes : array-like, shape (n_ticks,), dtype float or int
            Relative or absolute numbers of training examples that will be used to
            generate the learning curve. If the dtype is float, it is regarded as a
            fraction of the maximum size of the training set (that is determined
            by the selected validation method), i.e. it has to be within (0, 1].
            Otherwise it is interpreted as absolute sizes of the training sets.
            Note that for classification the number of samples usually have to
            be big enough to contain at least one sample from each class.
            (default: np.linspace(0.1, 1.0, 5))
        """
        plt.figure()
        plt.title(title)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, shuffle=False)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()

        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.legend(loc="best")

        return plt

    # Code utilized from Scikit learn.
    def plot_validation_curve(self, classifier, X, y, param_name, param_range=np.logspace(-6, -1, 5), cv=None):
        train_scores, test_scores = validation_curve(
            classifier, X, y, param_name=param_name, param_range=param_range,
            cv=cv, scoring="accuracy", n_jobs=1)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        ax = plt.figure().gca()
        plt.title("Validation Curve")
        plt.xlabel(param_name)
        plt.ylabel("Score")
        plt.ylim(0.0, 1.1)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        # lw = 2
        plt.plot(param_range, train_scores_mean, 'o-', linewidth=1, markersize=4, label="Training score",
                     color="darkorange")
        plt.fill_between(param_range, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.2,
                         color="darkorange")
        plt.plot(param_range, test_scores_mean, 'o-', linewidth=1, markersize=4, label="Cross-validation score",
                     color="navy")
        plt.fill_between(param_range, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.2,
                         color="navy")
        plt.legend(loc="best")
        filename = '{}/images/{}_{}_{}_MCC.png'.format('.', 'DT', 'BC', param_name)
        plt.savefig(filename, format='png', dpi=150)

        plt.close()

    def learn(self):
        label_encoder = preprocessing.LabelEncoder()
        encode=self.df[['Class']].copy()
        encode = encode.apply(label_encoder.fit_transform)
        self.df = self.df.drop(columns='Class')
        self.df = pd.concat([self.df, encode], axis=1)
        self.df = self.df[( self.df[['Clump Thickness','Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion','Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses','Class']] != '?').all(axis=1)]
        self.features = np.array(self.df.iloc[:, 0:-1])
        self.labels = np.array(self.df.iloc[:, -1])

        # Split the data into a training set and a test set
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.1, random_state=0, shuffle=False)
        scaler=preprocessing.StandardScaler().fit(X_train)
        X_train=scaler.transform(X_train)
        X_test=scaler.transform(X_test)

        self.classifier = tree.DecisionTreeClassifier()

        cv = 10;
        self.plot_learning_curve(self.classifier,"Learning curve", X_train,y_train,cv=cv)
        filename = '{}/images/{}_{}_LC.png'.format('.', 'DT', 'BC')
        plt.savefig(filename, format='png', dpi=150)
        plt.close()

        self.plot_validation_curve(tree.DecisionTreeClassifier(),X_train,y_train,"max_depth", np.arange(1,11,1), cv=cv)
        self.plot_validation_curve(tree.DecisionTreeClassifier(),X_train,y_train,"min_samples_leaf", np.arange(1,50,1), cv=cv)
        self.plot_validation_curve(tree.DecisionTreeClassifier(),X_train,y_train,"min_samples_split", np.arange(3,50,1), cv=cv)
        self.plot_validation_curve(tree.DecisionTreeClassifier(),X_train,y_train,"max_features", np.arange(2,10,1), cv=cv)


        parameters = {"min_samples_split": np.arange(3,30,1)}
        clf = GridSearchCV(tree.DecisionTreeClassifier(), parameters, cv=cv)
        clf.fit(X_train, y_train)
        print(clf.best_params_)

        self.classifier.set_params(**clf.best_params_)
        self.plot_learning_curve(self.classifier,"Learning curve-with optimised hyperparameter", X_train,y_train,cv=cv)
        filename = '{}/images/{}_{}_LC(optimized).png'.format('.', 'DT', 'BC')
        plt.savefig(filename, format='png', dpi=150)
        plt.close()

        self.classifier.fit(X_train, y_train)
        y_pred = self.classifier.predict(X_test)
        np.set_printoptions(precision=2)

        uniq=np.unique(self.labels)

        # Plot non-normalized confusion matrix
        self.plot_confusion_matrix(y_test, y_pred, uniq,
                              title='Confusion matrix, without normalization')

        filename = '{}/images/{}_{}_CM.png'.format('.', 'DT', 'BC')
        plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')

        # Plot normalized confusion matrix
        self.plot_confusion_matrix(y_test, y_pred, uniq, normalize=True,
                              title='Normalized confusion matrix')

        filename = '{}/images/{}_{}_CM_Normalized.png'.format('.', 'DT', 'BC')
        plt.savefig(filename, format='png', dpi=250,bbox_inches='tight')
        plt.close()


if __name__ == '__main__':
    dtlearner = decisionTreeLearner('./Datasets/Breast Cancer Classification/breast-cancer-wisconsin.csv')
    dtlearner.loadBCData()
    dtlearner.learn()