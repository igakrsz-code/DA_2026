import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import os
import warnings

warnings.filterwarnings("ignore")

class DataLoader:
    """Loads and merges the Fake and True news CSVs."""
    def __init__(self, fake_path: str, true_path: str):
        self.fake_path = fake_path
        self.true_path = true_path

    def load(self) -> pd.DataFrame:
        fake = pd.read_csv(self.fake_path)
        true = pd.read_csv(self.true_path)

        fake["label"] = "Fake"
        true["label"] = "Real"

        df = pd.concat([fake, true], ignore_index=True)
        print(f"✔ Loaded {len(fake):,} fake + {len(true):,} real articles.")
        return df

class FeatureEngineer:
    """Adds derived columns and cleans data for statistical analysis."""
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # 1. Length-based features (for T-tests)
        df["word_count"] = df["text"].astype(str).apply(lambda t: len(t.split()))
        
        # 2. Subject Normalization (CRITICAL for Chi-Squared)
        # The dataset has 'politics' and 'politicsNews'. We must group them to compare.
        df['subject'] = df['subject'].str.lower().replace({
            'politicsnews': 'politics',
            'worldnews': 'world',
            'government news': 'politics',
            'middle-east': 'world'
        })

        # 3. Clean Dates (Handle the messy strings in this dataset)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]) # Remove rows with invalid dates (e.g. URLs in date column)
        
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month

        print("✔ Features engineered: word_count, normalized subjects, and cleaned dates.")
        return df

class StatisticalAnalyzer:
    """Runs scipy-based significance tests as requested by the instructor."""
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.fake = df[df["label"] == "Fake"]
        self.real = df[df["label"] == "Real"]

    def run_analysis(self):
        print("\n── Statistical Significance Tests (SciPy) ─────────────")
        
        # 1. T-Test on Article Length
        t_stat, p_val_t = stats.ttest_ind(
            self.fake["word_count"], 
            self.real["word_count"], 
            equal_var=False
        )
        self._print_result("Welch's T-Test (Word Count)", p_val_t)

        # 2. Chi-Squared on Subject Distribution
        contingency = pd.crosstab(self.df["subject"], self.df["label"])
        chi2, p_val_chi, dof, _ = stats.chi2_contingency(contingency)
        self._print_result("Chi-Squared (Subject vs Label)", p_val_chi)

    def _print_result(self, test_name, p_val):
        sig = "✓ SIGNIFICANT" if p_val < 0.05 else "✗ NOT SIGNIFICANT"
        print(f" {test_name:<35} | p = {p_val:.6f} | {sig}")

class Visualizer:
    """Produces the visualizations for patterns and trends."""
    COLORS = {"Fake": "#e63946", "Real": "#2a9d8f"}

    def plot(self, df: pd.DataFrame, save_path: str):
        fig = plt.figure(figsize=(16, 10), facecolor="#0f0f14")
        gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.2)
        
        # A. Subject Distribution (Pattern Analysis)
        ax1 = fig.add_subplot(gs[0, 0])
        subj_data = df.groupby(["subject", "label"]).size().unstack(fill_value=0)
        subj_data.plot(kind="bar", ax=ax1, color=[self.COLORS["Fake"], self.COLORS["Real"]], alpha=0.8)
        self._style(ax1, "Subject Distribution by Authenticity", "Subject", "Count")

        # B. Article Length Distribution
        ax2 = fig.add_subplot(gs[0, 1])
        for label, color in self.COLORS.items():
            sns_data = df[df["label"] == label]["word_count"].clip(upper=2000)
            ax2.hist(sns_data, bins=50, alpha=0.5, color=color, label=label)
        self._style(ax2, "Word Count Distribution (Capped at 2k)", "Words", "Frequency")
        ax2.legend()

        # C. Publishing Trends (Time Analysis)
        ax3 = fig.add_subplot(gs[1, :])
        trend = df.groupby([df['date'].dt.to_period('M'), 'label']).size().unstack(fill_value=0)
        trend.index = trend.index.to_timestamp()
        for label in trend.columns:
            ax3.plot(trend.index, trend[label], color=self.COLORS[label], label=label, lw=2)
        self._style(ax3, "Publishing Trends (2015-2018)", "Date", "Articles")
        
        plt.savefig(save_path, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"✔ Visualization saved to {save_path}")

    def _style(self, ax, title, xlabel, ylabel):
        ax.set_facecolor("#1a1a2e")
        ax.set_title(title, color="white", fontweight="bold")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")

class AnalysisPipeline:
    """Orchestrates the analysis tool."""
    def __init__(self, fake_path, true_path):
        self.loader = DataLoader(fake_path, true_path)
        self.engineer = FeatureEngineer()
        self.visualizer = Visualizer()

    def run(self):
        df = self.loader.load()
        df = self.engineer.transform(df)
        
        # Run the stats Yossi asked for
        analyzer = StatisticalAnalyzer(df)
        analyzer.run_analysis()
        
        # Generate the plots
        self.visualizer.plot(df, "news_analysis_report.png")
        print("\n✔ Analysis Complete. Ready for Hackathon presentation.")

if __name__ == "__main__":
  
    pipeline = AnalysisPipeline("Fake.csv", "True.csv")
    pipeline.run()
