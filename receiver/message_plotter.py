import matplotlib.pyplot as plt
import os
import sys
from tkinter import filedialog, Tk

def visualize_message(file_path):
    """
    Reads the receiver's recording file containing pure binary sequences
    and plots the full sequence of bits.
    """
    all_bits = []

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                line_bits = [int(b) for b in line if b in ('0', '1')]
                all_bits.extend(line_bits)

        if not all_bits:
            print("No binary data found in the file.")
            return

        # Statistics
        total_count = len(all_bits)
        ones_count = sum(all_bits)
        zeros_count = total_count - ones_count
        
        stats_info = (
            f"Signal Analysis:\n"
            f"Total bits: {total_count}\n"
            f"Ones (1): {ones_count} ({ (ones_count/total_count)*100:.1f}%)\n"
            f"Zeros (0): {zeros_count} ({ (zeros_count/total_count)*100:.1f}%)"
        )

        # Plotting
        plt.figure(figsize=(15, 5))
        plt.step(range(len(all_bits)), all_bits, where='post', color="#9d15a6", linewidth=1)
        
        plt.title(f'Recorded message - {os.path.basename(file_path)}', fontsize=14)
        plt.xlabel('Index')
        plt.ylabel('LED State')
        plt.ylim(-0.2, 1.2)
        plt.yticks([0, 1], ['0 (OFF)', '1 (ON)'])
        plt.grid(True, which='both', linestyle='--', alpha=0.5)

        text_props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
        plt.text(0.01, 0.95, stats_info, transform=plt.gca().transAxes, fontsize=10,
                 verticalalignment='top', bbox=text_props, family='monospace')

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    target_file = None

    # Check if a filename was passed as a command-line argument
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # If no argument, open a File Selection Dialog
        print("No file provided. Opening file selector...")
        root = Tk()
        root.withdraw()
        target_file = filedialog.askopenfilename(
            title="Select a recording file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        root.destroy()

    if target_file:
        visualize_message(target_file)
    else:
        print("No file selected. Exiting.")

