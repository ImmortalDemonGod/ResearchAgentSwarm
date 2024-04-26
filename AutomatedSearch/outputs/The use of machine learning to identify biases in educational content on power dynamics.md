# The Use of Machine Learning to Identify Biases in Educational Content on Power Dynamics

## Introduction

In recent years, there has been a growing concern about biases in educational content, particularly related to power dynamics. Biases in educational materials can perpetuate existing inequalities and reinforce power imbalances among different groups of students. To address this issue, researchers have turned to machine learning algorithms as a potential solution. Machine learning algorithms have the ability to analyze large amounts of data and identify patterns and biases that may not be immediately apparent to human observers.

This report aims to explore the use of machine learning algorithms in identifying biases in educational content, specifically focusing on power dynamics. We will examine existing methodologies, analyze case studies, and propose potential solutions to address these biases. By understanding the current state of research and the challenges involved, we can gain insights into how machine learning can be leveraged to create more equitable educational environments.

## Methodologies for Identifying Biases

### Adjusting Sample Weights

One common strategy for identifying biases in educational content is to adjust sample weights. This approach involves assigning different weights to different samples based on their demographic characteristics or other relevant factors. By doing so, researchers can ensure that the algorithm takes into account the representation of different groups and avoids over-representing or under-representing certain demographics.

### Bias Attenuation Methods

Another approach is to use bias attenuation methods, which aim to reduce the impact of biases in the algorithm's decision-making process. These methods involve modifying the algorithm's training process or the data it uses to train. For example, researchers may introduce additional training data that represents under-represented groups or apply techniques such as data augmentation to create a more balanced dataset.

### Fairness Through Un/Awareness

Fairness through un/awareness is a strategy that involves making the algorithm unaware of certain sensitive attributes, such as gender or race, during the training process. By removing or hiding these attributes from the algorithm, researchers aim to prevent the algorithm from making biased decisions based on these attributes. However, it is important to note that this approach may not always be feasible or appropriate, as some attributes may be inherently relevant to the educational context.

### Adversarial Learning

Adversarial learning is a technique that involves training two competing models: one model tries to predict the target variable, while the other model tries to predict the sensitive attribute. By training these models simultaneously, researchers can identify and mitigate biases in the algorithm's decision-making process. Adversarial learning has shown promising results in various domains, including education, by explicitly addressing biases and promoting fairness.

## Case Studies

### Student Dropout Prediction

One area where machine learning algorithms have been applied to identify biases in educational content is student dropout prediction. Predicting student dropout is a crucial task for educational institutions to provide timely interventions and support to at-risk students. However, biases in the data used for training these algorithms can lead to unfair predictions and exacerbate existing inequalities.

In a study by Rets et al. (2023), the researchers investigated the fairness of machine learning algorithms in predicting student dropout in distance education. They found that biases in the data, such as gender and socioeconomic status, influenced the algorithm's predictions. To address these biases, the researchers proposed adjusting the sample weights based on these demographic attributes and using bias attenuation methods to create a more balanced dataset. The results showed that these strategies improved the fairness of the algorithm's predictions.

### Performance Prediction

Machine learning algorithms have also been used to predict student performance in educational settings. However, biases in the data used for training these algorithms can lead to inaccurate predictions and reinforce existing inequalities. In a study by Sha et al. (2022), the researchers leveraged class balancing techniques to alleviate algorithmic bias in predictive tasks related to student performance. By balancing the representation of different groups in the training data, the researchers were able to reduce biases and improve the accuracy and fairness of the algorithm's predictions.

### Forum Post Classification

Another area where biases in educational content can be identified using machine learning algorithms is forum post classification. Educational forums provide a platform for students to engage in discussions and seek help from their peers and instructors. However, biases in the classification algorithms used to categorize forum posts can lead to unequal treatment and hinder students' access to relevant information.

In a study by Sha et al. (2021), the researchers assessed the algorithmic fairness of automatic classifiers for educational forum posts. They found that the classifiers exhibited biases in their predictions, with certain groups of students being more likely to receive incorrect classifications. To address these biases, the researchers proposed using bias attenuation methods and adversarial learning techniques. The results showed that these strategies improved the fairness of the classifiers and reduced the disparities in classification accuracy among different groups.

## Challenges and Recommendations

While machine learning algorithms show promise in identifying biases in educational content, there are several challenges that need to be addressed. One major challenge is the availability of representative and unbiased training data. Biases in the training data can propagate through the algorithm and result in biased predictions. Therefore, it is crucial to ensure that the training data is diverse, balanced, and representative of the student population.

Another challenge is the interpretability of machine learning algorithms. Many machine learning models, such as deep neural networks, are often considered black boxes, making it difficult to understand how they arrive at their predictions. This lack of interpretability can hinder the identification and mitigation of biases. Researchers and developers should strive to develop more interpretable models and techniques that allow for a better understanding of the decision-making process.

Furthermore, it is important to consider the ethical implications of using machine learning algorithms in educational settings. The use of algorithms to make decisions about students' educational opportunities raises concerns about privacy, fairness, and accountability. It is crucial to establish clear guidelines and regulations to ensure that the use of machine learning algorithms in education is ethical and respects students' rights.

To address these challenges, it is recommended to adopt a context-specific approach to ensure equitable treatment in educational settings. This involves considering the specific characteristics and needs of the student population and tailoring the algorithmic solutions accordingly. Additionally, ongoing monitoring and evaluation of the algorithms' performance and fairness are essential to identify and rectify any biases that may arise.

## Conclusion

Machine learning algorithms have the potential to identify biases in educational content related to power dynamics. By leveraging techniques such as adjusting sample weights, bias attenuation methods, fairness through un/awareness, and adversarial learning, researchers can mitigate biases and promote fairness in educational settings. However, there are challenges that need to be addressed, including the availability of representative training data and the interpretability of machine learning models. By considering these challenges and implementing context-specific approaches, we can work towards creating more equitable educational environments.

## References

Ali, M., Sapiezynski, P., Bogen, M., Korolova, A., Mislove, A., & Rieke, A. (2019). Discrimination through optimization: How Facebook’s ad delivery can Lead to biased outcomes. Proceedings of the ACM on Human-Computer Interaction, 3(CSCW). [Link](https://doi.org/10.1145/3359301)

Anderson, H., Boodhwani, A., & Baker, R. S. (2019). Assessing the fairness of graduation predictions. Proceedings of the 12th International Conference on Educational Data Mining, 488–491.

Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). Machine Bias: there’s software used across the country to predict future criminals. And it’s biased against blacks. ProPublica. [Link](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing%0A)

Arroyo, I., Burleson, W., Tai, M., Muldner, K., & Woolf, B. P. (2013). Gender differences in the use and benefit of advanced learning Technologies for Mathematics. Journal of Educational Psychology, 105(4), 957–969. [Link](https://doi.org/10.1037/a0032748)

ASSISTments Project. (2014). ASSISTmentsData: Terms of Use for Using Data. Retrieved January 7, 2021, from [Link](https://sites.google.com/site/assistmentsdata/termsofuseforusingdata)

Mayfield, E., Madaio, M., Prabhumoye, S., Gerritsen, D., McLaughlin, B., Dixon-Román, E., & Black, A. W. (2019). Equity Beyond Bias in Language Technologies for Education. Proceedings of the Fourteenth Workshop on Innovative Use of NLP for Building Educational Applications, 444–460. [Link](https://doi.org/10.18653/v1/W19-4446)

Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2019). A survey on Bias and fairness in machine learning. ArXiv E-Prints, arXiv:1908.09635. [Link](https://arxiv.org/abs/1908.09635)

Melis, E., Goguadze, G., Libbrecht, P., & Ullrich, C. (2009). Culturally adapted mathematics education with ActiveMath. AI & SOCIETY, 24(3), 251–265. [Link](https://doi.org/10.1007/s00146-009-0215-4)

Milliron, M. D., Malcolm, L., & Kil, D. (2014). Insight and action analytics: Three case studies to consider. Research & Practice in Assessment, 9, 70–89.

Ryan S. Baker & Aaron Hawn. (2023). Algorithmic Bias in Education. Learning Analytics and Fairness: Do Existing Algorithms Serve Everyone Equally?

Jamiu Adekunle Idowu. (2023). Experts’ View on Challenges and Needs for Fairness in Artificial Intelligence for Education. Evolution and Revolution in Artificial Intelligence in Education. Ido Roll & Ruth Wylie.

Decades of psychological research clearly show that once humans inherit a bias or encounter misinformation, those beliefs are hard to revise. Celeste Kidd, PhD, an assistant professor of psychology at the University of California, Berkeley, argues that assumptions about AI’s capabilities, as well as the way many tools present information in a conversational, matter-of-fact way, make the risk of inheriting stubborn biases particularly high (Science, Vol. 380, 2023).

“The conversation about AI bias is broadening,” said psychologist Tara Behrend, PhD, a professor at Michigan State University’s School of Human Resources and Labor Relations who studies human-technology interaction and spoke at CES about AI and privacy. “Agencies and various academic stakeholders are really taking the role of psychology seriously.”

Browse the latest updates from APA, informed by psychological science.

News
Highlights
Advocacy
Support psychology. Improve lives.
Addressing equity and ethics in artificial intelligence
Algorithms and humans both contribute to bias in AI, but AI may also hold the power to correct or reverse inequities among humans
Vol. 55 No. 3
Print version: page 24
As artificial intelligence (AI) rapidly permeates our world, researchers and policymakers are scrambling to stay one step ahead. What are the potential harms of these new tools—and how can they be avoided?
“With any new technology, we always need to be thinking about what’s coming next. But AI is moving so fast that it’s difficult to grasp how significantly it’s going to change things,” said David Luxton, PhD, a clinical psychologist and an affiliate professor at the University of Washington’s School of Medicine who spoke at the 2024 Consumer Electronics Show (CES) on Harnessing the Power of AI Ethically.

“There’s a lot of pushback against AI because it can promote bias, but humans have been promoting biases for a really long time,” said psychologist Rhoda Au, PhD, a professor of anatomy and neurobiology at the Boston University Chobanian & Avedisian School of Medicine who also spoke at CES on harnessing AI ethically. “We can’t just be dismissive and say: ‘AI is good’ or ‘AI is bad.’ We need to embrace its complexity and understand that it’s going to be both.”

With that complexity in mind, world leaders are exploring how to maximize the benefits of AI and minimize its harms. In 2023, the Biden administration released an executive order on Safe, Secure, and Trustworthy AI and the European Union came close to passing its first comprehensive AI Act. Psychologists, with their expertise on cognitive biases and cultural inclusion, as well as in measuring the reliability and representativeness of datasets—have a growing role in those discussions.

## The Future of AI in Higher Education

According to the 2024 EDUCAUSE AI Landscape Study, respondents are optimistic about the potential for AI to positively impact the future of higher education while recognizing several areas of concern. Respondents believe that academic dishonesty will increase (64%) and that students will trust AI tools too much (60%). Respondents were equivocal about whether AI outputs will become more or less biased. These results suggest that respondents are optimistic about the potential for AI to positively impact the future of higher education while recognizing several areas of concern.

The higher education community is still looking for common ground on how AI should and should not be used for learning and work. Respondents were asked to describe both appropriate and inappropriate uses of AI in higher education. In general, respondents emphasized the ethical and transparent use of AI, no matter the specific application. One respondent summarized, "AI should be embraced as an emerging technology and should have a place in coursework with focus on implementation, adoption, research, utilization, and ethical and legal considerations."

## Does AI Have a Bias Problem?

Research has shown that as AI tools are growing in their scope and abilities to mimic characteristics of human intelligence, their biases are expanding as well. AI bias refers to algorithms that “produce biased results that reflect and perpetuate human biases within a society, including historical and current social inequality.” AI bias has been seen to negatively affect non-native English speakers, where their written work is falsely flagged as AI-generated and could lead to accusations of cheating. AI bias can also affect job opportunities, financial decisions, and healthcare outcomes.

## The Ethical Implications of AI Bias

The ethical implications of AI bias are of great concern. Biased AI systems can perpetuate discrimination and unfairness, affecting opportunities in areas such as employment, finance, and healthcare. Lack of accountability in biased AI decision-making processes poses challenges in taking corrective action. These systems can inadvertently reinforce societal stereotypes, deepening social divides and hindering progress toward a more equitable society. Legal and regulatory concerns regarding the accountability and fairness of AI systems further underscore the urgency of addressing bias.

## Conclusion

In conclusion, the use of machine learning algorithms to identify biases in educational content related to power dynamics holds great potential for creating more equitable educational environments. By employing strategies such as adjusting sample weights, bias attenuation methods, fairness through un/awareness, and adversarial learning, researchers can mitigate biases and promote fairness in educational settings. However, challenges such as the availability of representative training data and the interpretability of machine learning models need to be addressed. By considering these challenges and implementing context-specific approaches, we can work towards creating a more inclusive and equitable education system.

References:

1. Ali, M., Sapiezynski, P., Bogen, M., Korolova, A., Mislove, A., & Rieke, A. (2019). Discrimination through optimization: How Facebook’s ad delivery can Lead to biased outcomes. Proceedings of the ACM on Human-Computer Interaction, 3(CSCW). [Link](https://doi.org/10.1145/3359301)

2. Anderson, H., Boodhwani, A., & Baker, R. S. (2019). Assessing the fairness of graduation predictions. Proceedings of the 12th International Conference on Educational Data Mining, 488–491.

3. Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). Machine Bias: there’s software used across the country to predict future criminals. And it’s biased against blacks. ProPublica. [Link](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing%0A)

4. Arroyo, I., Burleson, W., Tai, M., Muldner, K., & Woolf, B. P. (2013). Gender differences in the use and benefit of advanced learning Technologies for Mathematics. Journal of Educational Psychology, 105(4), 957–969. [Link](https://doi.org/10.1037/a0032748)

5. ASSISTments Project. (2014). ASSISTmentsData: Terms of Use for Using Data. Retrieved January 7, 2021, from [Link](https://sites.google.com/site/assistmentsdata/termsofuseforusingdata)

6. Mayfield, E., Madaio, M., Prabhumoye, S., Gerritsen, D., McLaughlin, B., Dixon-Román, E., & Black, A. W. (2019). Equity Beyond Bias in Language Technologies for Education. Proceedings of the Fourteenth Workshop on Innovative Use of NLP for Building Educational Applications, 444–460. [Link](https://doi.org/10.18653/v1/W19-4446)

7. Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2019). A survey on Bias and fairness in machine learning. ArXiv E-Prints, arXiv:1908.09635. [Link](https://arxiv.org/abs/1908.09635)

8. Melis, E., Goguadze, G., Libbrecht, P., & Ullrich, C. (2009). Culturally adapted mathematics education with ActiveMath. AI & SOCIETY, 24(3), 251–265. [Link](https://doi.org/10.1007/s00146-009-0215-4)

9. Milliron, M. D., Malcolm, L., & Kil, D. (2014). Insight and action analytics: Three case studies to consider. Research & Practice in Assessment, 9, 70–89.

10. Ryan S. Baker & Aaron Hawn. (2023). Algorithmic Bias in Education. Learning Analytics and Fairness: Do Existing Algorithms Serve Everyone Equally?

11. Jamiu Adekunle Idowu. (2023). Experts’ View on Challenges and Needs for Fairness in Artificial Intelligence for Education. Evolution and Revolution in Artificial Intelligence in Education. Ido Roll & Ruth Wylie.