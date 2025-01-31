import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import subprocess

def run_popper_and_get_metrics():
    """Run Popper and extract metrics from output."""
    try:
        # Run Popper and capture output
        cmd = ['python3', 'Popper/popper.py', 'popper_main/', '--debug']
        print(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print complete output for debugging
        print("\nPopper STDOUT:")
        print(result.stdout)
        print("\nPopper STDERR:")
        print(result.stderr)
        
        # Look for the solution section
        solution_match = re.search(r'\*{10}\s*SOLUTION\s*\*{10}(.*?)\*{10}', 
                                 result.stdout, re.DOTALL)
        
        if solution_match:
            solution_text = solution_match.group(1).strip()
            print("\nFound solution section:")
            print(solution_text)
            
            # Extract metrics from solution section
            metrics_match = re.search(r'Precision:([\d.]+)\s+Recall:([\d.]+)\s+TP:(\d+)\s+FN:(\d+)\s+TN:(\d+)\s+FP:(\d+)', 
                                    solution_text)
            
            if metrics_match:
                metrics = {
                    'precision': float(metrics_match.group(1)),
                    'recall': float(metrics_match.group(2)),
                    'tp': int(metrics_match.group(3)),
                    'fn': int(metrics_match.group(4)),
                    'tn': int(metrics_match.group(5)),
                    'fp': int(metrics_match.group(6))
                }
                print("\nExtracted metrics:", metrics)
                return metrics
                
        # If we get here, we couldn't find the metrics
        print("\nCouldn't extract metrics using regular expressions.")
        print("Please check if the Popper output format has changed.")
        return None
            
    except Exception as e:
        print(f"\nError running Popper: {str(e)}")
        return None

def create_confusion_matrix(metrics):
    """Create confusion matrix visualization from metrics."""
    if not metrics:
        print("No metrics provided")
        return
        
    # Create the confusion matrix
    cm = np.array([[metrics['tp'], metrics['fn']],
                  [metrics['fp'], metrics['tn']]])
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(1, 3)
    
    # Confusion Matrix (larger)
    ax1 = fig.add_subplot(gs[0, :2])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Predicted Positive', 'Predicted Negative'],
                yticklabels=['Actual Positive', 'Actual Negative'], ax=ax1)
    ax1.set_title('Confusion Matrix', pad=20)
    
    # Add text annotations
    descriptions = {
        'TP': f"True Positives: {metrics['tp']}\nCorrectly identified positive examples",
        'FN': f"False Negatives: {metrics['fn']}\nMissed positive examples",
        'FP': f"False Positives: {metrics['fp']}\nIncorrectly identified as positive",
        'TN': f"True Negatives: {metrics['tn']}\nCorrectly identified negative examples"
    }
    
    # Add text box with descriptions
    description_text = '\n\n'.join([f"{k}: {v}" for k, v in descriptions.items()])
    ax1.text(2.5, 0.5, description_text, bbox=dict(facecolor='white', alpha=0.8), 
             fontsize=10, transform=ax1.transAxes)
    
    # Metrics visualization
    ax2 = fig.add_subplot(gs[0, 2])
    metrics_to_plot = {
        'Precision': metrics['precision'],
        'Recall': metrics['recall']
    }
    
    # Plot metrics
    colors = ['skyblue', 'lightgreen']
    bars = ax2.bar(metrics_to_plot.keys(), metrics_to_plot.values(), color=colors)
    ax2.set_ylim(0, 1.2)
    ax2.set_title('Performance Metrics')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    # Add grid
    ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add formulas
    formulas = (f'Precision = TP/(TP+FP) = {metrics["tp"]}/({metrics["tp"]}+{metrics["fp"]})\n'
                f'Recall = TP/(TP+FN) = {metrics["tp"]}/({metrics["tp"]}+{metrics["fn"]})')
    ax2.text(0.5, -0.2, formulas, ha='center', va='center', 
             transform=ax2.transAxes, bbox=dict(facecolor='white', alpha=0.8))
    
    # Add overall accuracy
    total = sum(metrics[k] for k in ['tp', 'tn', 'fp', 'fn'])
    accuracy = (metrics['tp'] + metrics['tn']) / total if total > 0 else 0
    plt.figtext(0.98, 0.02, f'Overall Accuracy: {accuracy:.2%}', 
                ha='right', va='bottom')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('confusion_matrix_analysis_2.png', bbox_inches='tight', dpi=300)
    plt.close()

    # Print detailed metrics report
    print(f"\nDetailed Metrics Report:")
    print("="*50)
    print(f"True Positives (TP): {metrics['tp']} - Correctly identified positive examples")
    print(f"False Negatives (FN): {metrics['fn']} - Missed positive examples")
    print(f"False Positives (FP): {metrics['fp']} - Incorrectly identified as positive")
    print(f"True Negatives (TN): {metrics['tn']} - Correctly identified negative examples")
    print("-"*50)
    print(f"Precision: {metrics['precision']:.2f} - Accuracy of positive predictions")
    print(f"Recall: {metrics['recall']:.2f} - Proportion of actual positives identified")
    print(f"Overall Accuracy: {accuracy:.2%}")
    print("="*50)

if __name__ == "__main__":
    print("Starting confusion matrix generation...")
    metrics = run_popper_and_get_metrics()
    
    if metrics:
        print("\nGenerating visualization...")
        create_confusion_matrix(metrics)
        print("\nVisualization saved as 'confusion_matrix_analysis.png'")
    else:
        print("\nFailed to generate confusion matrix due to missing metrics")