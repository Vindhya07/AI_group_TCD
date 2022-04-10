import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import FormatStrFormatter


def plot1():
    rows=[]
    with open("dfs_values.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)

    # MCTS Plotting
    mcts_rows=[]
    with open("mcts_values.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        mcts_header = next(csvreader)
        for row in csvreader:
            mcts_rows.append(row)

    # Genetic Plotting
    genetic_rows=[]
    with open("genetic_values.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        genetic_header = next(csvreader)
        for row in csvreader:
            genetic_rows.append(row)

    # print(header)
    # print(rows)
    # fig, ((ax1, ax3, ax5), (ax2, ax4, ax6)) = plt.subplots(2, 3, figsize=(10, 10))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))

    # DFS plotting
    # print(genetic_rows[0])
    ax1.plot(rows[1], color="magenta", label="Deep First Search")
    ax1.plot(mcts_rows[1], color="blue", label="MCTS")
    ax1.plot(genetic_rows[0], genetic_rows[1], color="orange", label="Genetic")
    ax1.set_xlabel("Time Taken (ms)")
    ax1.set_ylabel("Score")
    ax1.set_title("Time Taken vs Score")
    xticks = ax1.get_xticks()
    ax1.set_xticks(xticks[::len(xticks) // 5])
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax1.get_yticks()
    ax1.set_yticks(yticks[::len(yticks) // 8])
    ax1.legend()


    ax2.plot(rows[2], color="magenta", label="Deep First Search")
    ax2.plot(mcts_rows[2], color="blue", label="MCTS")
    ax2.plot(genetic_rows[0], genetic_rows[2], color="orange", label="Genetic")
    ax2.set_xlabel("Time Taken (ms)")
    ax2.set_ylabel("Lines Cleared")
    ax2.set_title("Time Taken vs Lines Cleared")
    xticks = ax2.get_xticks()
    ax2.set_xticks(xticks[::len(xticks) // 5])
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax2.get_yticks()
    ax2.set_yticks(yticks[::len(yticks) // 8])
    ax2.legend()

    plt.show()

def plot2():
    rows=[]
    with open("dfs_values.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)

    # MCTS Plotting
    mcts_rows=[]
    with open("mcts_values.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        mcts_header = next(csvreader)
        for row in csvreader:
            mcts_rows.append(row)

    # Genetic Plotting
    genetic_rows=[]
    with open("genetic_values.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        genetic_header = next(csvreader)
        for row in csvreader:
            genetic_rows.append(row)

    fig, ((ax1, ax3, ax5), (ax2, ax4, ax6)) = plt.subplots(2, 3, figsize=(10, 10))
    # fig.tight_layout()
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.5)



    # DFS plotting
    ax1.plot(rows[0], rows[1], color="magenta", label="Deep First Search")
    ax1.set_xlabel("Time Taken (ms)")
    ax1.set_ylabel("Score")
    ax1.set_title("DFS: \n Time Taken vs Score")
    xticks = ax1.get_xticks()
    ax1.set_xticks(xticks[::len(xticks) // 5])
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax1.get_yticks()
    ax1.set_yticks(yticks[::len(yticks) // 8])
    ax1.legend()


    ax2.plot(rows[0], rows[2], color="magenta", label="Deep First Search")
    ax2.set_xlabel("Time Taken (ms)")
    ax2.set_ylabel("Lines Cleared")
    ax2.set_title("DFS: \n Time Taken vs Lines Cleared")
    xticks = ax2.get_xticks()
    ax2.set_xticks(xticks[::len(xticks) // 5])
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax2.get_yticks()
    ax2.set_yticks(yticks[::len(yticks) // 8])
    ax2.legend()

    ax3.plot(mcts_rows[0], mcts_rows[1], color="blue", label="MCTS")
    ax3.set_xlabel("Time Taken (ms)")
    ax3.set_ylabel("Score")
    xticks = ax3.get_xticks()
    ax3.set_xticks(xticks[::len(xticks) // 5])
    ax3.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax3.get_yticks()
    ax3.set_yticks(yticks[::len(yticks) // 8])
    ax3.set_title("MCTS: \n Time Taken vs Score")
    ax3.legend()


    ax4.plot(mcts_rows[0], mcts_rows[2], color="blue", label="MCTS")
    ax4.set_xlabel("Time Taken (ms)")
    ax4.set_ylabel("Lines Cleared")
    xticks = ax4.get_xticks()
    ax4.set_xticks(xticks[::len(xticks) // 5])
    ax4.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax4.get_yticks()
    ax4.set_yticks(yticks[::len(yticks) // 8])
    ax4.set_title("MCTS: \n Time Taken vs Lines Cleared")
    ax4.legend()

    ax5.plot(genetic_rows[0], genetic_rows[1], color="orange", label="Genetic")
    ax5.set_xlabel("Time Taken (ms)")
    ax5.set_ylabel("Score")
    xticks = ax5.get_xticks()
    ax5.set_xticks(xticks[::len(xticks) // 5])
    ax5.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax5.get_yticks()
    ax5.set_yticks(yticks[::len(yticks) // 8])
    ax5.set_title("Genetic: \n Time Taken vs Score")
    ax5.legend()


    ax6.plot(genetic_rows[0], genetic_rows[2], color="orange", label="Genetic")
    ax6.set_xlabel("Time Taken (ms)")
    ax6.set_ylabel("Lines Cleared")
    xticks = ax6.get_xticks()
    ax6.set_xticks(xticks[::len(xticks) // 5])
    ax6.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    yticks = ax6.get_yticks()
    ax6.set_yticks(yticks[::len(yticks) // 8])
    ax6.set_title("Genetic: \n Time Taken vs Lines CLeared")
    ax6.legend()

    plt.show()

plot1()
plot2()
