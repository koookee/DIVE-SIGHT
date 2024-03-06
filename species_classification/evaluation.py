import matplotlib.pyplot as plt
import numpy as np

# In descending order of the threshold values
true_positives = [0, 554, 595, 608, 618, 624, 629, 632, 636, 636, 637]
false_negatives = [637, 83, 42, 29, 19, 13, 8, 5, 1, 1, 0]
false_positives = [0, 482, 905, 1205, 1513, 1825, 2188, 2640, 3236, 3983, 4305]
true_negatives = [4305, 3823, 3400, 3100, 2792, 2480, 2117, 1665, 1069, 322, 0]


def plot_roc():
    thresholds = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    true_positive_rates = []
    false_positive_rates = []
    precision_rates = []
    recall_rates = []
    for i in range(0, 11):
        true_positive_rates.append(true_positives[i] / (true_positives[i] + false_negatives[i]))
        false_positive_rates.append(false_positives[i] / (false_positives[i] + true_negatives[i]))

        if true_positives[i] == 0 and false_positives[i] == 0: 
            precision_rates.append(1)
        else:
            precision_rates.append(true_positives[i] / (true_positives[i] + false_positives[i]))

        recall_rates.append(true_positives[i] / (true_positives[i] + false_negatives[i]))
    
    true_positive_rates = np.array(true_positive_rates)
    false_positive_rates = np.array(false_positive_rates)
    precision_rates = np.array(precision_rates)
    recall_rates = np.array(recall_rates)
    thresholds = np.array(thresholds)

    f1_scores = 2 * (precision_rates * recall_rates) / (precision_rates + recall_rates)
    max_f1_index = np.argmax(f1_scores)
    plt.plot(thresholds, f1_scores)
    plt.xlabel('Threshold')
    plt.ylabel('F1 Score')
    plt.title('F1 Score vs Threshold')
    plt.grid(True)
    plt.ylim(0, 1)
    plt.annotate(f'Max F1 Score = {f1_scores[max_f1_index]:.2f}\nThreshold = {thresholds[max_f1_index]:.2f}',
             xy=(thresholds[max_f1_index], f1_scores[max_f1_index]),
             xytext=(thresholds[max_f1_index] - 0.4, f1_scores[max_f1_index]),
             fontsize=10)
    plt.show()


    auc = np.trapz(true_positive_rates, false_positive_rates)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.annotate(f'AUC = {auc:.2f}', xy=(0.6, 0.4), xytext=(0.7, 0.6),
             fontsize=12)
    plt.plot(false_positive_rates, true_positive_rates)
    plt.grid(True)
    plt.show()

    plt.plot(recall_rates, precision_rates)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.grid(True)
    plt.show()

plot_roc()