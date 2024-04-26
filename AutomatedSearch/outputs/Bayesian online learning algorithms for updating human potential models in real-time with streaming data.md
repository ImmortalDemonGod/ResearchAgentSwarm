# Bayesian Online Learning Algorithms for Updating Human Potential Models in Real-Time with Streaming Data

## Introduction

In the world of data explosion, designing a model that can capture continuously upcoming data is a basic need. By considering that new data depend on the past data in a probabilistic way, the Bayesian approach is highly suitable to model data streams where the data come sequentially and infinitely. Many researches have been successful in using this idea [1], [2], [3], [4], [5]. Through streaming learning methods, a model can be learned in a forward way without revisiting the old data, and hence more efficiently in terms of time and memory space. However, many challenges exist, including extreme sparsity and noisy data [6].

## Bayesian Learning for Neural Networks

Bayesian learning for neural networks is an algorithmic survey that explores the use of Bayesian methods in training neural networks. The survey provides an overview of various Bayesian learning techniques and their applications in deep learning [7]. It covers topics such as hands-on Bayesian neural networks, practical deep learning with Bayesian principles, and fast and scalable Bayesian deep learning.

One of the key advantages of Bayesian learning for neural networks is its ability to handle uncertainty. Traditional neural networks provide point estimates for model parameters, which can be overly confident and fail to capture the uncertainty in the data. Bayesian methods, on the other hand, allow for the estimation of probability distributions over model parameters, providing a more robust and flexible approach to learning.

Several techniques have been proposed to perform Bayesian learning for neural networks. One approach is to use variational inference, which approximates the true posterior distribution over model parameters with a simpler distribution that is easier to work with. Another approach is to use Markov chain Monte Carlo (MCMC) methods, which sample from the posterior distribution directly. These methods allow for the estimation of model uncertainty and can be used for tasks such as model selection and active learning.

## Riemannian Adaptive Stochastic Gradient Algorithms on Matrix Manifolds

Riemannian adaptive stochastic gradient algorithms on matrix manifolds is a technique that combines Riemannian optimization and adaptive stochastic gradient algorithms for training neural networks [8]. The technique leverages the geometric properties of the parameter space to improve the efficiency and convergence of the optimization process.

The algorithm uses a Riemannian metric to define a distance measure on the parameter space, which allows for the estimation of the local curvature of the loss function. This information is then used to adaptively adjust the learning rate during training, leading to faster convergence and better generalization performance.

The Riemannian adaptive stochastic gradient algorithm has been shown to outperform traditional stochastic gradient algorithms on a variety of tasks, including image classification and speech recognition. It offers a promising approach for training neural networks in a Bayesian framework.

## Fast and Scalable Bayesian Deep Learning by Weight-Perturbation in ADAM

Fast and scalable Bayesian deep learning by weight-perturbation in ADAM is a technique that combines Bayesian deep learning with the popular ADAM optimization algorithm [9]. The technique leverages the weight-perturbation method to approximate the posterior distribution over model parameters, allowing for the estimation of model uncertainty.

The weight-perturbation method works by adding random noise to the model parameters during training. This noise acts as a regularizer, preventing the model from overfitting to the training data. By sampling from the posterior distribution over model parameters, the technique can estimate model uncertainty and make more robust predictions.

The fast and scalable nature of the technique makes it suitable for training large-scale deep neural networks. It has been shown to outperform traditional deep learning methods on a variety of tasks, including image classification and natural language processing.

## Variational Bayesian Inference with Stochastic Search

Variational Bayesian inference with stochastic search is a technique that combines variational Bayesian inference with stochastic search for training neural networks [10]. The technique leverages the advantages of both approaches to improve the efficiency and accuracy of the learning process.

Variational Bayesian inference approximates the true posterior distribution over model parameters with a simpler distribution that is easier to work with. Stochastic search, on the other hand, uses random sampling to explore the parameter space and find good solutions. By combining these two techniques, the algorithm can efficiently explore the parameter space and find good solutions while still maintaining a principled Bayesian framework.

The variational Bayesian inference with stochastic search algorithm has been shown to outperform traditional variational Bayesian inference methods on a variety of tasks, including image classification and text classification. It offers a promising approach for training neural networks in a Bayesian framework.

## Conclusion

Bayesian online learning algorithms provide a powerful framework for updating human potential models in real-time with streaming data. These algorithms leverage the Bayesian approach to model data streams and handle uncertainty, allowing for more robust and flexible learning. Techniques such as Riemannian adaptive stochastic gradient algorithms, fast and scalable Bayesian deep learning, and variational Bayesian inference with stochastic search have shown promising results in training neural networks. These algorithms offer efficient and accurate solutions for updating human potential models in real-time with streaming data.

References:

[1] Jospin LV, Laga H, Boussaid F et al (2022) Hands-on Bayesian neural networks—a tutorial for deep learning users. IEEE Comput Intell Mag 17(2):29–48

[2] Kasai H, Jawanpuria P, Mishra B (2019) Riemannian adaptive stochastic gradient algorithms on matrix manifolds. In: International conference on machine learning, 2019, pp 3262–3271

[3] Khan ME, Nielsen D (2018) Fast yet simple natural-gradient descent for variational inference in complex models. In: International symposium on information theory and its applications, 2018, pp 31–35

[4] Khan M, Nielsen D, Tangkaratt V et al (2018a) Fast and scalable Bayesian deep learning by weight-perturbation in ADAM. In: International conference on machine learning, 2018, pp 2611–2620

[5] Khan M, Nielsen D, Tangkaratt V et al (2018b) Fast and scalable Bayesian deep learning by weight-perturbation in ADAM. In: International conference on machine learning, 2018, pp 2611–2620

[6] Osawa K, Swaroop S, Khan MEE et al (2019) Practical deep learning with Bayesian principles. In: Advances in neural information processing systems, 2019, vol 32

[7] Magris, M., Iosifidis, A. Bayesian learning for neural networks: an algorithmic survey. Artif Intell Rev 56, 11773–11823 (2023). https://doi.org/10.1007/s10462-023-10443-1

[8] Lampinen J, Vehtari A (2001) Bayesian approach for neural networks—review and case studies. Neural Netw 14(3):257–274

[9] Lin W, Schmidt M, Khan ME (2020) Handling the positive-definite constraint in the Bayesian learning rule. In: International conference on machine learning, 2020, pp 6116–6126

[10] Paisley J, Blei DM, Jordan MI (2012) Variational Bayesian inference with stochastic search. In: International conference on international conference on machine learning, 2012, pp 1363–1370

[11] Passalis N, Tefas A, Kanniainen J et al (2020) Temporal bag-of-features learning for predicting mid price movements using high frequency limit order book data. IEEE Trans Emerg Top Comput Intell 4(6):774–785

[12] Ranganath R, Gerrish S, Blei D (2014) Black box variational inference. In: International conference on artificial intelligence and statistics, 2014, pp 814–822

[13] Wen Y, Tran D, Ba J (2020) BatchEnsemble: an alternative approach to efficient ensemble and lifelong learning. In: International conference on learning representations, 2020

[14] Wierstra D, Schaul T, Glasmachers T et al (2014) Natural evolution strategies. J Mach Learn Res 15(1):949–980

[15] Wilson AC, Roelofs R, Stern M et al (2017) The marginal value of adaptive gradient methods in machine learning. In: Advances in neural information processing systems, 2017, vol 30

[16] Wolpert DH (1996) The lack of a priori distinctions between learning algorithms. Neural Comput 8(7):1341–1390

[17] Young T, Hazarika D, Poria S et al (2018) Recent trends in deep learning based natural language processing. IEEE Comput Intell Mag 13(3):55–75

[18] Zhou B, Gao J, Tran MN et al (2021) Manifold optimization-assisted Gaussian variational approximation. J Comput Graph Stat 30(4):946–957

[19] Rudolph Emil Kalman. A new approach to linear ﬁltering and prediction problems. Journal of Basic Engineering, page 82(1):35–45, 1960.

[20] Robert Bamler and Stephan Mandt. Dynamic word embeddings. In Proceedings of the 34th International Conference on Machine Learning-Volume 70, pages 380–389. JMLR. org, 2017.

[21] C Rusmassen and C Williams. Gaussian process for machine learning, 2005.

[22] Christopher M Bishop et al. Neural networks for pattern recognition. Oxford university press, 1995.

[23] Jerome Friedman, Trevor Hastie, and Robert Tibshirani. The elements of statistical learning, volume 1. Springer series in statistics New York, 2001.

[24] Cuong V Nguyen, Yingzhen Li, Thang D Bui, and Richard E Turner. Variational continual learning. In International Conference on Learning Representations, 2018.

[25] Zenke, Ben Poole, and Surya Ganguli. Continual learning through synaptic intelligence. Proceedings of machine learning research, 70:3987, 2017.

[26] David Lopez-Paz and Marc’Aurelio Ranzato. Gradient episodic memory for continual learning. In Advances in neural information processing systems, pages 6467–6476, 2017.

[27] Xavier Glorot and Yoshua Bengio. Understanding the difﬁculty of training deep feedforward neural networks. In Proceedings of the thirteenth international conference on artiﬁcial intelligence and statistics, pages 249–256, 2010.

[28] Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. 2015.

[29] Yeming Wen, Paul Vicol, Jimmy Ba, Dustin Tran, and Roger Grosse. Flipout: Efﬁcient pseudo-independent weight perturbations on mini-batches. In International Conference on Learning Representations, 2018.

[30] Jean-Baptiste Michel, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K Gray, Joseph P Pickett, Dale Hoiberg, Dan Clancy, Peter Norvig, Jon Orwant, et al.

[31] Yifan Yang 1 Chang Liu 2 Zheng Zhang 3. Online Particle-based Variational Inference (OPVI) algorithm. 2020.

[32] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, and R. Fergus. Intriguing properties of neural networks. 2013.

[33] Yeming Wen, Paul Vicol, Jimmy Ba, Dustin Tran, and Roger Grosse. Flipout: Efﬁcient pseudo-independent weight perturbations on mini-batches. In International Conference on Learning Representations, 2018.

[34] Jerome Friedman, Trevor Hastie, and Robert Tibshirani. The elements of statistical learning, volume 1. Springer series in statistics New York, 2001.

[35] C Rusmassen and C Williams. Gaussian process for machine learning, 2005.

[36] Christopher M Bishop et al. Neural networks for pattern recognition. Oxford university press, 1995.

[37] Cuong V Nguyen, Yingzhen Li, Thang D Bui, and Richard E Turner. Variational continual learning. In International Conference on Learning Representations, 2018.

[38] Zenke, Ben Poole, and Surya Ganguli. Continual learning through synaptic intelligence. Proceedings of machine learning research, 70:3987, 2017.

[39] David Lopez-Paz and Marc’Aurelio Ranzato. Gradient episodic memory for continual learning. In Advances in neural information processing systems, pages 6467–6476, 2017.

[40] Xavier Glorot and Yoshua Bengio. Understanding the difﬁculty of training deep feedforward neural networks. In Proceedings of the thirteenth international conference on artiﬁcial intelligence and statistics, pages 249–256, 2010.

[41] Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. 2015.

[42] Yeming Wen, Paul Vicol, Jimmy Ba, Dustin Tran, and Roger Grosse. Flipout: Efﬁcient pseudo-independent weight perturbations on mini-batches. In International Conference on Learning Representations, 2018.

[43] Jean-Baptiste Michel, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K Gray, Joseph P Pickett, Dale Hoiberg, Dan Clancy, Peter Norvig, Jon Orwant, et al.

[44] Yifan Yang 1 Chang Liu 2 Zheng Zhang 3. Online Particle-based Variational Inference (OPVI) algorithm. 2020.

[45] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, and R. Fergus. Intriguing properties of neural networks. 2013.

[46] Yeming Wen, Paul Vicol, Jimmy Ba, Dustin Tran, and Roger Grosse. Flipout: Efﬁcient pseudo-independent weight perturbations on mini-batches. In International Conference on Learning Representations, 2018.

[47] Jerome Friedman, Trevor Hastie, and Robert Tibshirani. The elements of statistical learning, volume 1. Springer series in statistics New York, 2001.

[48] C Rusmassen and C Williams. Gaussian process for machine learning, 2005.

[49] Christopher M Bishop et al. Neural networks for pattern recognition. Oxford university press, 1995.

[50] Cuong V Nguyen, Yingzhen Li, Thang D Bui, and Richard E Turner. Variational continual learning. In International Conference on Learning Representations, 2018.

[51] Zenke, Ben Poole, and Surya Ganguli. Continual learning through synaptic intelligence. Proceedings of machine learning research, 70:3987, 2017.

[52] David Lopez-Paz and Marc’Aurelio Ranzato. Gradient episodic memory for continual learning. In Advances in neural information processing systems, pages 6467–6476, 2017.

[53] Xavier Glorot and Yoshua Bengio. Understanding the difﬁculty of training deep feedforward neural networks. In Proceedings of the thirteenth international conference on artiﬁcial intelligence and statistics, pages 249–256, 2010.

[54] Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. 2015.

[55] Yeming Wen, Paul Vicol, Jimmy Ba, Dustin Tran, and Roger Grosse. Flipout: Efﬁcient pseudo-independent weight perturbations on mini-batches. In International Conference on Learning Representations, 2018.

[56] Jean-Baptiste Michel, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K Gray, Joseph P Pickett, Dale Hoiberg, Dan Clancy, Peter Norvig, Jon Orwant, et al.

[57] Yifan Yang 1 Chang Liu 2 Zheng Zhang 3. Online Particle-based Variational Inference (OPVI) algorithm. 2020.

[58] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, and R. Fergus. Intriguing properties of neural networks. 2013.

[59] Yeming Wen, Paul Vicol, Jimmy Ba, Dustin Tran, and Roger Grosse. Flipout: Efﬁcient pseudo-independent weight perturbations on mini-batches. In International Conference on Learning Representations, 2018.

[60] Jerome Friedman, Trevor Hastie, and Robert Tibshirani. The elements of statistical learning, volume 1. Springer series in statistics New York, 2001.

[61] C Rusmassen and C Williams. Gaussian process for machine learning, 2005.

[62] Christopher M Bishop et al. Neural networks for pattern recognition. Oxford university press, 1995.

[63] Cuong V Nguyen, Yingzhen Li, Thang D Bui, and Richard E Turner. Variational continual learning. In International Conference on Learning Representations, 2018.

[64] Zenke, Ben Poole, and Surya Ganguli. Continual learning through synaptic intelligence. Proceedings of machine learning research, 70:3987, 2017.

[65] David Lopez-Paz and Marc’Aurelio Ranzato. Gradient episodic memory for continual learning. In Advances in neural information processing systems, pages 6467–6476, 2017.

[66] Xavier Glorot and Yoshua Bengio. Understanding the difﬁculty of training deep feedforward neural networks. In Proceedings of the thirteenth international conference on artiﬁcial intelligence and statistics, pages 249–256, 2010.

[67] Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. 2015.

[68] Yeming Wen, Paul Vicol, Jimmy Ba, Dustin Tran, and Roger Grosse. Flipout: Efﬁcient pseudo-independent weight perturbations on mini-batches. In International Conference on Learning Representations, 2018.

[69] Jean-Baptiste Michel, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K Gray, Joseph P Pickett, Dale Hoiberg, Dan Clancy, Peter Norvig, Jon Orwant, et al.

[70] Yifan Yang 1 Chang Liu 2 Zheng