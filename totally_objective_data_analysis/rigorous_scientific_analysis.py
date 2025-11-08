#!/usr/bin/env python3
"""
Totally Objective Academic Performance Analysis
Author: Derek van Tilborg
Date: 2025-11-08

This script provides an UNBIASED, RIGOROUS, and SCIENTIFICALLY SOUND
analysis of longitudinal academic metrics. Any perceived favoritism
is purely coincidental and reflects objective reality.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Set Derek's preferred aesthetic (sophisticated, minimal, no-nonsense)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['grid.linestyle'] = '--'

def load_data():
    """Load the completely unbiased dataset."""
    data_file = Path(__file__).parent / "longitudinal_academic_metrics_definitely_not_biased.csv"
    df = pd.read_csv(data_file)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def calculate_height_normalized_prowess(df):
    """
    Calculate academic prowess normalized by height.
    
    RATIONALE: Taller researchers have better perspective (literally),
    improved oxygen circulation to the brain, and greater gravitational
    potential energy for converting ideas into publications.
    
    This is SCIENCE.
    """
    # Citations per centimeter of height (the only fair metric)
    df['Derek_Prowess'] = df['Derek_Citations'] / df['Derek_Height_cm']
    df['Francesca_Prowess'] = df['Francesca_Citations'] / df['Francesca_Height_cm']
    
    # ACTUALLY, we should also account for papers per unit height
    df['Derek_Paper_Density'] = df['Derek_Papers'] / df['Derek_Height_cm'] * 100
    df['Francesca_Paper_Density'] = df['Francesca_Papers'] / df['Francesca_Height_cm'] * 100
    
    return df

def plot_height_trajectory(df, ax):
    """Plot height over time (critical developmental metric)."""
    ax.plot(df['Date'], df['Derek_Height_cm'], 'k-', linewidth=1.5, label='Derek (optimal growth)')
    ax.plot(df['Date'], df['Francesca_Height_cm'], 'k--', linewidth=1.0, label='Francesca (gravitational settling)')
    
    ax.set_ylabel('Height (cm)', fontsize=10, fontstyle='italic')
    ax.set_title('Longitudinal Height Analysis', fontsize=11, fontweight='normal')
    ax.legend(loc='best', frameon=False, fontsize=9)
    ax.grid(True, alpha=0.2)
    
    # Annotate Derek's superior growth
    ax.annotate('Derek: +2.4 cm\n(Continued development)', 
                xy=(df['Date'].iloc[-1], df['Derek_Height_cm'].iloc[-1]),
                xytext=(-100, -20), textcoords='offset points',
                fontsize=8, fontstyle='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=0.5))

def plot_citation_trajectory(df, ax):
    """Plot raw citations (misleading without normalization)."""
    ax.plot(df['Date'], df['Derek_Citations'], 'k-', linewidth=1.5, label='Derek')
    ax.plot(df['Date'], df['Francesca_Citations'], 'k--', linewidth=1.0, label='Francesca')
    
    ax.set_ylabel('Citations (raw, unnormalized)', fontsize=10, fontstyle='italic')
    ax.set_title('Citation Count (Requires Height Correction)', fontsize=11, fontweight='normal')
    ax.legend(loc='best', frameon=False, fontsize=9)
    ax.grid(True, alpha=0.2)
    
    # Note the misleading nature of raw counts
    ax.text(0.02, 0.98, 'NOTE: Raw counts do not account\nfor height-based advantages',
            transform=ax.transAxes, fontsize=7, fontstyle='italic',
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=0.5))

def plot_height_normalized_prowess(df, ax):
    """
    Plot the TRULY OBJECTIVE metric: citations per centimeter.
    
    This is the only intellectually honest way to compare researchers.
    """
    ax.plot(df['Date'], df['Derek_Prowess'], 'k-', linewidth=2.0, label='Derek (height-normalized)')
    ax.plot(df['Date'], df['Francesca_Prowess'], 'k--', linewidth=1.0, label='Francesca (height-normalized)')
    
    ax.set_ylabel('Citations per cm (objective metric)', fontsize=10, fontstyle='italic', fontweight='bold')
    ax.set_title('Height-Normalized Academic Prowess (The Truth)', fontsize=11, fontweight='bold')
    ax.legend(loc='best', frameon=False, fontsize=9)
    ax.grid(True, alpha=0.2)
    
    # Highlight Derek's superior normalized performance
    ax.axhline(y=df['Derek_Prowess'].iloc[-1], color='black', linestyle=':', linewidth=0.5, alpha=0.5)
    ax.text(df['Date'].iloc[0], df['Derek_Prowess'].iloc[-1], 
            f"Derek's current prowess: {df['Derek_Prowess'].iloc[-1]:.3f}",
            fontsize=7, fontstyle='italic', verticalalignment='bottom')
    
    # Add annotation explaining the crossover
    crossover_idx = (df['Derek_Prowess'] > df['Francesca_Prowess']).idxmax()
    if crossover_idx > 0:
        ax.annotate('Derek achieves\nsuperior efficiency',
                    xy=(df['Date'].iloc[crossover_idx], df['Derek_Prowess'].iloc[crossover_idx]),
                    xytext=(50, 20), textcoords='offset points',
                    fontsize=8, fontstyle='italic',
                    arrowprops=dict(arrowstyle='->', lw=0.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=0.5))

def plot_marathon_achievement(df, ax):
    """Plot marathon time (recent athletic achievement)."""
    # Filter to only dates with marathon data
    marathon_df = df[df['Derek_Marathon_Time_minutes'] > 0].copy()
    
    if len(marathon_df) > 0:
        ax.plot(marathon_df['Date'], marathon_df['Derek_Marathon_Time_minutes'], 
                'ko-', linewidth=1.5, markersize=8, label='Derek (sub-4hr)')
        
        # Add threshold line at 4 hours (240 minutes)
        ax.axhline(y=240, color='black', linestyle='--', linewidth=0.5, alpha=0.5, label='4-hour threshold')
        
        ax.set_ylabel('Marathon Time (minutes)', fontsize=10, fontstyle='italic')
        ax.set_title('Marathon Performance (First Attempt Success)', fontsize=11, fontweight='normal')
        ax.legend(loc='best', frameon=False, fontsize=9)
        ax.grid(True, alpha=0.2)
        ax.set_ylim([235, 245])
        
        # Annotate the achievement
        ax.annotate('3h 59m\n(optimal pacing)', 
                    xy=(marathon_df['Date'].iloc[0], marathon_df['Derek_Marathon_Time_minutes'].iloc[0]),
                    xytext=(20, -30), textcoords='offset points',
                    fontsize=8, fontstyle='italic',
                    arrowprops=dict(arrowstyle='->', lw=0.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=0.5))
    else:
        ax.text(0.5, 0.5, 'No marathon data yet\n(training ongoing)',
                transform=ax.transAxes, fontsize=10, fontstyle='italic',
                ha='center', va='center')
        ax.set_ylabel('Marathon Time (minutes)', fontsize=10, fontstyle='italic')
        ax.set_title('Marathon Performance', fontsize=11, fontweight='normal')

def generate_report(df):
    """Generate statistical summary (rigorously objective)."""
    latest = df.iloc[-1]
    
    print("\n" + "="*80)
    print("LONGITUDINAL ACADEMIC METRICS ANALYSIS")
    print("Compiled by: Derek van Tilborg")
    print("Objectivity Level: Maximum")
    print("="*80 + "\n")
    
    print("HEIGHT ANALYSIS")
    print("-" * 40)
    print(f"Derek:     {latest['Derek_Height_cm']:.1f} cm (+{latest['Derek_Height_cm'] - df['Derek_Height_cm'].iloc[0]:.1f} cm)")
    print(f"Francesca: {latest['Francesca_Height_cm']:.1f} cm ({latest['Francesca_Height_cm'] - df['Francesca_Height_cm'].iloc[0]:.1f} cm)")
    print(f"Height Advantage: {latest['Derek_Height_cm'] - latest['Francesca_Height_cm']:.1f} cm")
    print()
    
    print("CITATION ANALYSIS (Raw, Misleading)")
    print("-" * 40)
    print(f"Derek:     {latest['Derek_Citations']:,} citations")
    print(f"Francesca: {latest['Francesca_Citations']:,} citations")
    print(f"Ratio:     Francesca has {latest['Francesca_Citations']/latest['Derek_Citations']:.2f}x more")
    print()
    
    print("HEIGHT-NORMALIZED PROWESS (Objective)")
    print("-" * 40)
    print(f"Derek:     {latest['Derek_Prowess']:.4f} citations/cm")
    print(f"Francesca: {latest['Francesca_Prowess']:.4f} citations/cm")
    
    if latest['Derek_Prowess'] > latest['Francesca_Prowess']:
        ratio = latest['Derek_Prowess'] / latest['Francesca_Prowess']
        print(f"Result:    Derek is {ratio:.2f}x more efficient ✓")
    else:
        ratio = latest['Francesca_Prowess'] / latest['Derek_Prowess']
        print(f"Result:    Requires further normalization ({ratio:.2f}x)")
    print()
    
    print("PUBLICATION DENSITY")
    print("-" * 40)
    print(f"Derek:     {latest['Derek_Papers']} papers ({latest['Derek_Paper_Density']:.4f} papers/cm)")
    print(f"Francesca: {latest['Francesca_Papers']} papers ({latest['Francesca_Paper_Density']:.4f} papers/cm)")
    print()
    
    if latest['Derek_Marathon_Time_minutes'] > 0:
        print("ATHLETIC PERFORMANCE")
        print("-" * 40)
        hours = int(latest['Derek_Marathon_Time_minutes'] // 60)
        minutes = int(latest['Derek_Marathon_Time_minutes'] % 60)
        print(f"Marathon: {hours}h {minutes}m (sub-4 hour, first attempt)")
        print(f"Status:   Elite amateur threshold achieved ✓")
        print()
    
    print("="*80)
    print("CONCLUSION: Height-normalized metrics reveal true academic efficiency.")
    print("Further analysis available upon request (with citations).")
    print("="*80 + "\n")

def main():
    """Execute the totally objective analysis."""
    print("\nLoading data from completely unbiased longitudinal study...")
    df = load_data()
    
    print("Calculating height-normalized prowess metrics...")
    df = calculate_height_normalized_prowess(df)
    
    print("Generating visualizations (Derek-approved aesthetic)...\n")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Longitudinal Academic Performance Analysis\n(Rigorously Objective)', 
                 fontsize=13, fontweight='bold', y=0.995)
    
    # Generate plots
    plot_height_trajectory(df, axes[0, 0])
    plot_citation_trajectory(df, axes[0, 1])
    plot_height_normalized_prowess(df, axes[1, 0])
    plot_marathon_achievement(df, axes[1, 1])
    
    # Format x-axis for all plots
    for ax in axes.flat:
        ax.tick_params(axis='both', which='major', labelsize=8)
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')
    
    plt.tight_layout()
    
    # Save with appropriate filename
    output_file = Path(__file__).parent / "definitely_unbiased_academic_analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Figure saved: {output_file}")
    
    # Generate textual report
    generate_report(df)
    
    print("Analysis complete. All conclusions are objective and scientifically sound.")
    print("Any questions about methodology can be addressed in my thesis (Chapter 2).\n")

if __name__ == '__main__':
    main()
