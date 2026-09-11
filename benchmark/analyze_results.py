"""Generate summary tables and chart from raw benchmark CSV."""
import pandas as pd
import matplotlib.pyplot as plt


def analyze(csv_path: str, output_dir: str = "."):
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} rows")

    # Summary table
    summary = df.groupby('system').agg(
        pass_rate=('verdict', lambda x: (x == 'PASS').mean() * 100),
        avg_coverage=('coverage', 'mean'),
        avg_retries=('retries', 'mean'),
        avg_time=('time', 'mean')
    ).round(2).reset_index()
    summary = summary.sort_values('avg_coverage', ascending=False)
    summary.to_csv(f"{output_dir}/results_summary.csv", index=False)
    print(summary.to_string(index=False))

    # By category
    cat = df.pivot_table(
        index='category', columns='system',
        values='coverage', aggfunc='mean'
    ).round(1)
    cat.to_csv(f"{output_dir}/results_by_category.csv")
    print(cat.to_string())

    # Chart
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    colors = ['#d9954a' if s == 'HDAFA' else '#888' for s in summary['system']]
    axes[0].bar(summary['system'], summary['pass_rate'], color=colors)
    axes[0].set_title('Pass Rate (%)')
    axes[0].set_ylim(0, 105)
    axes[0].tick_params(axis='x', rotation=45)

    axes[1].bar(summary['system'], summary['avg_coverage'], color=colors)
    axes[1].set_title('Avg Coverage (%)')
    axes[1].set_ylim(0, 105)
    axes[1].tick_params(axis='x', rotation=45)

    axes[2].bar(summary['system'], summary['avg_time'], color=colors)
    axes[2].set_title('Avg Time (s)')
    axes[2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/results_chart.png", dpi=150, bbox_inches='tight')
    print("✅ results_chart.png saved")


if __name__ == "__main__":
    analyze("hdafa_baselines_gemini.csv")
