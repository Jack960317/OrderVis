# ReorderVis
It's a interface for ReorderVis, a tool that can rise the explainability of your Rnn Model.


这个系统分为两个部分——浏览器部分browser side和机器学习部分machine learning side。其中机器学习部分计算用户输入的预测值以及输出的预测值相关的可解释性的信息，
机器学习部分可以直接运行提供一部分的可解释性，而browser side则负责可视化、交互的功能，在机器学习部分的基础上大大提升可解释性。如果需要使用我们的系统，需要分
别在同一台或两台机器上运行这两个部分 browser side 和 machine learning side。这两个系统的代码已放在相对应的同名分支下了，请点击branch查看。
