#!/usr/bin/env python3
"""
Main entry point for the Glass Data Science Project
Phelps et al. 2016 Dataset Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from pathlib import Path

# Add src to Python path for imports
sys.path.append('src')


def main():
    """Main function to run the data science analysis"""

    print("🔬 Glass Data Science Project")
    print("=" * 50)

    # Set up paths
    data_path = Path("data/raw/Phelps2016.xlsx")

    # Check if data file exists
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        print("Please make sure your Excel file is in the data/raw/ directory")
        return

    try:
        # Load the dataset
        print(f"📊 Loading data from {data_path}...")
        df = pd.read_excel(data_path)
        print(f"✅ Data loaded successfully!")

        # Basic dataset information
        print(f"\nDataset Info:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")

        # Display first few rows
        print(f"\nFirst 5 rows:")
        print(df.head())

        # Basic statistics
        print(f"\nBasic Statistics:")
        print(df.describe())

        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            print(f"\n⚠️  Missing Values:")
            print(missing_data[missing_data > 0])
        else:
            print(f"\n✅ No missing values found")

        # Data types
        print(f"\nData Types:")
        print(df.dtypes.value_counts())

        # Try to create a simple visualization
        try:
            # Set up matplotlib
            plt.style.use('default')

            # Get numerical columns
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

            if len(numerical_cols) > 0:
                print(f"\n📈 Creating basic visualizations...")

                # Create results directory if it doesn't exist
                results_dir = Path("results/figures")
                results_dir.mkdir(parents=True, exist_ok=True)

                # Distribution plot for first numerical column
                plt.figure(figsize=(10, 6))
                first_col = numerical_cols[0]
                plt.hist(df[first_col].dropna(), bins=30, alpha=0.7, edgecolor='black')
                plt.title(f'Distribution of {first_col}')
                plt.xlabel(first_col)
                plt.ylabel('Frequency')
                plt.grid(True, alpha=0.3)

                # Save the plot
                plot_path = results_dir / f"{first_col}_distribution.png"
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.close()
                print(f"✅ Saved plot: {plot_path}")

                # Correlation heatmap if multiple numerical columns
                if len(numerical_cols) > 1:
                    plt.figure(figsize=(10, 8))
                    correlation_matrix = df[numerical_cols].corr()
                    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
                                center=0, square=True, fmt='.2f')
                    plt.title('Correlation Matrix')
                    plt.tight_layout()

                    # Save correlation plot
                    corr_path = results_dir / "correlation_matrix.png"
                    plt.savefig(corr_path, dpi=300, bbox_inches='tight')
                    plt.close()
                    print(f"✅ Saved correlation plot: {corr_path}")

        except Exception as e:
            print(f"⚠️  Could not create visualizations: {e}")

        # Try Ollama integration (if available)
        try:
            from ollama_helper import setup_ollama
            print(f"\n🤖 Testing AI integration...")

            ai = setup_ollama("llama2")

            # Create a summary for AI analysis
            data_summary = f"""
            Dataset: Phelps et al. 2016
            Shape: {df.shape[0]} rows, {df.shape[1]} columns
            Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}
            Data types: {df.dtypes.value_counts().to_dict()}
            Missing values: {df.isnull().sum().sum()}
            """

            # Ask AI for suggestions (with timeout)
            suggestion = ai.ask(f"Based on this dataset summary, what analysis should I start with? {data_summary}")

            if suggestion:
                print(f"\n🧠 AI Suggestions:")
                print(suggestion)
            else:
                print(f"⚠️  AI service not available")

        except ImportError:
            print(f"⚠️  Ollama helper not available (run in Docker for AI features)")
        except Exception as e:
            print(f"⚠️  AI integration error: {e}")

        print(f"\n🎉 Analysis complete!")
        print(f"\nNext steps:")
        print(f"1. Open Jupyter Lab: http://localhost:8888 (if using Docker)")
        print(f"2. Create notebooks in the notebooks/ directory")
        print(f"3. Check results in results/figures/ directory")
        print(f"4. Use the AI helper for analysis suggestions")

        return df

    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None


def setup_environment():
    """Set up the project environment"""

    # Create necessary directories
    directories = [
        "data/raw",
        "data/processed",
        "data/external",
        "notebooks",
        "src",
        "results/figures",
        "results/reports"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print(f"✅ Project directories created")


def check_dependencies():
    """Check if required packages are installed"""

    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn',
        'openpyxl', 'requests'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print(f"Run: pip install {' '.join(missing_packages)}")
        return False
    else:
        print(f"✅ All required packages installed")
        return True


if __name__ == "__main__":
    print(f"🚀 Starting Glass Data Science Project")

    # Setup environment
    setup_environment()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Run main analysis
    df = main()

    # Keep the dataframe available for interactive use
    if df is not None:
        print(f"\n💡 Tip: DataFrame is available as 'df' variable")
        print(f"Try: df.info(), df.describe(), df.head()")