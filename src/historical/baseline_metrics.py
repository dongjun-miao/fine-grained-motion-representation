import numpy as np


def classification_metrics(labels, scores, num_classes=52):
    labels, scores = np.asarray(labels, dtype=np.int64), np.asarray(scores)
    if scores.shape != (len(labels), num_classes) or not len(labels):
        raise ValueError('Invalid labels/scores shape')
    if np.any(labels < 0) or np.any(labels >= num_classes) or not np.isfinite(scores).all():
        raise ValueError('Invalid labels/scores values')
    ranked = np.argsort(-scores, axis=1, kind='stable')
    predicted = ranked[:, 0]
    confusion = np.zeros((num_classes, num_classes), dtype=np.int64)
    np.add.at(confusion, (labels, predicted), 1)
    true_positive = confusion.diagonal().astype(np.float64)
    support = confusion.sum(1)
    predicted_counts = confusion.sum(0)
    f1 = np.divide(2*true_positive, support + predicted_counts,
                   out=np.zeros(num_classes), where=(support + predicted_counts) > 0)
    recall = np.divide(true_positive, support, out=np.zeros(num_classes), where=support > 0)
    return dict(top1=float(np.mean(predicted == labels)),
                top5=float(np.mean((ranked[:, :min(5, num_classes)] == labels[:, None]).any(1))),
                macro_f1=float(f1.mean()), balanced_accuracy=float(recall[support > 0].mean()),
                samples=len(labels), support=support.tolist(), per_class_f1=f1.tolist(),
                per_class_recall=recall.tolist(), confusion_matrix=confusion.tolist())
