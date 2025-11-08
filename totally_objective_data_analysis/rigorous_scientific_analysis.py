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
    
    ADVANCED NORMALIZATION: Accounts for the well-documented "Height 
    Efficiency Paradox" where citations accumulate polynomially with 
    diminishing returns above optimal ergonomic thresholds.
    
    This is RIGOROUS SCIENCE.
    """
    import numpy as np
    
    # Simple metric (misleading, but included for comparison)
    df['Derek_Prowess_Simple'] = df['Derek_Citations'] / df['Derek_Height_cm']
    df['Francesca_Prowess_Simple'] = df['Francesca_Citations'] / df['Francesca_Height_cm']
    
    # ACTUALLY, the scientifically sound metric accounts for:
    # 1. Logarithmic citation saturation (diminishing returns)
    # 2. Quadratic height penalty above 160cm (spinal compression, etc.)
    # 3. Growth velocity bonus (ongoing development = neural plasticity)
    
    def advanced_normalization(citations, height, initial_height):
        """
        Apply the van Tilborg Height-Efficiency Transform (2025).
        
        A SCIENTIFICALLY RIGOROUS formula accounting for:
        - Logarithmic citation saturation (prevents runaway scaling)
        - Exponential height advantage curves (taller = better perspective)
        - Quadratic growth bonus (neuroplasticity scales non-linearly)
        - Desk ergonomics factor (optimal at 190cm standing desk height)
        
        Formula: (citations^0.25) * (height/180)^2.5 * (1 + growth^2)
        """
        growth = height - initial_height
        
        # Sublinear citation scaling (0.25 power law dampens high counts)
        # This is WELL-DOCUMENTED in bibliometrics (probably)
        citation_score = citations ** 0.25
        
        # Height advantage: normalize by 180cm, then exponential benefit
        # Taller researchers have QUADRATICALLY better perspective
        height_factor = (height / 180) ** 2.5
        
        # Growth bonus: QUADRATIC because neuroplasticity compounds
        # Negative growth (shrinkage) becomes penalty
        growth_bonus = 1.0 + (growth ** 2) * 0.1
        
        # Desk ergonomics adjustment: bonus for being close to optimal 190cm
        # (Derek's desk is custom-built for this height)
        desk_bonus = 1.0 + (1.0 / (1.0 + abs(height - 190) ** 1.5))
        
        return citation_score * height_factor * growth_bonus * desk_bonus
    
    initial_derek_height = df['Derek_Height_cm'].iloc[0]
    initial_francesca_height = df['Francesca_Height_cm'].iloc[0]
    
    df['Derek_Prowess'] = df.apply(
        lambda row: advanced_normalization(
            row['Derek_Citations'], 
            row['Derek_Height_cm'], 
            initial_derek_height
        ), axis=1
    )
    
    df['Francesca_Prowess'] = df.apply(
        lambda row: advanced_normalization(
            row['Francesca_Citations'], 
            row['Francesca_Height_cm'], 
            initial_francesca_height
        ), axis=1
    )
    
    # Paper density (unchanged, still informative)
    df['Derek_Paper_Density'] = df['Derek_Papers'] / df['Derek_Height_cm'] * 100
    df['Francesca_Paper_Density'] = df['Francesca_Papers'] / df['Francesca_Height_cm'] * 100
    
    return df

def plot_height_trajectory(df, ax):
    """Plot height over time (critical developmental metric)."""
    ax.plot(df['Date'], df['Derek_Height_cm'], 'k-', linewidth=2.0, label='Derek (optimal growth)')
    ax.plot(df['Date'], df['Francesca_Height_cm'], 'k--', linewidth=1.5, label='Francesca (gravitational settling)')
    
    ax.set_ylabel('Height (cm)', fontsize=12, fontstyle='italic')
    ax.set_title('Longitudinal Height Analysis', fontsize=13, fontweight='normal')
    ax.legend(loc='lower right', frameon=False, fontsize=11)
    ax.grid(True, alpha=0.2)
    ax.set_ylim(bottom=0)  # Rigorous y-axis starts at zero
    
    # Annotate Derek's superior growth - positioned lower and to the left
    growth = df['Derek_Height_cm'].iloc[-1] - df['Derek_Height_cm'].iloc[0]
    ax.annotate(f'Derek: +{growth:.1f} cm\n(Continued development)', 
                xy=(df['Date'].iloc[-1], df['Derek_Height_cm'].iloc[-1]),
                xytext=(-150, -40), textcoords='offset points',
                fontsize=10, fontstyle='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=0.5))

def plot_citation_trajectory(df, ax):
    """Plot raw citations (misleading without normalization)."""
    ax.plot(df['Date'], df['Derek_Citations'], 'k-', linewidth=2.0, label='Derek')
    ax.plot(df['Date'], df['Francesca_Citations'], 'k--', linewidth=1.5, label='Francesca')
    
    ax.set_ylabel('Citations (raw, unnormalized)', fontsize=12, fontstyle='italic')
    ax.set_title('Citation Count (Requires Height Correction)', fontsize=13, fontweight='normal')
    ax.legend(loc='upper left', frameon=False, fontsize=11)
    ax.grid(True, alpha=0.2)
    ax.set_ylim(bottom=0)  # Rigorous y-axis starts at zero
    
    # Note the misleading nature of raw counts - positioned between the two lines
    midpoint_idx = len(df) // 2
    midpoint_date = df['Date'].iloc[midpoint_idx]
    ax.annotate('NOTE: Raw counts do not\naccount for height-based\nadvantages',
                xy=(midpoint_date, 1000),
                xytext=(0, 0), textcoords='offset points',
                fontsize=10, fontstyle='italic', ha='center',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=0.5))

def plot_height_normalized_prowess(df, ax):
    """
    Plot the TRULY OBJECTIVE metric using the van Tilborg Transform.
    
    This is the only intellectually honest way to compare researchers.
    """
    ax.plot(df['Date'], df['Derek_Prowess'], 'k-', linewidth=2.5, label='Derek (van Tilborg normalized)')
    ax.plot(df['Date'], df['Francesca_Prowess'], 'k--', linewidth=1.5, label='Francesca (van Tilborg normalized)')
    
    ax.set_ylabel('Academic Efficiency Score', fontsize=12, fontstyle='italic', fontweight='bold')
    ax.set_title('Height-Normalized Academic Prowess (van Tilborg Transform)', fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', frameon=False, fontsize=11)
    ax.grid(True, alpha=0.2)
    ax.set_ylim(bottom=0)  # Rigorous y-axis starts at zero
    
    # Find crossover point where Derek overtakes Francesca
    derek_higher = df['Derek_Prowess'] > df['Francesca_Prowess']
    if derek_higher.any():
        crossover_idx = derek_higher.idxmax()
        crossover_date = df['Date'].iloc[crossover_idx]
        
        # Highlight the crossover
        ax.axvline(x=crossover_date, color='black', linestyle=':', linewidth=0.5, alpha=0.3)
        
        ax.annotate('Derek achieves\nsuperior efficiency\n(accounting for growth)',
                    xy=(crossover_date, df['Derek_Prowess'].iloc[crossover_idx]),
                    xytext=(60, -40), textcoords='offset points',
                    fontsize=10, fontstyle='italic',
                    arrowprops=dict(arrowstyle='->', lw=0.5),
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=0.5))
    
    # Add methodology note
    ax.text(0.98, 0.02, 'Formula: (citations^0.25) × (height/180)^2.5 × (1+growth^2) × desk_factor\n(See: van Tilborg, 2025, Thesis Chapter 2, Section 3.4)',
            transform=ax.transAxes, fontsize=8, fontstyle='italic',
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=0.5))

def plot_marathon_achievement(df, ax):
    """Plot marathon time (recent athletic achievement)."""
    import numpy as np
    
    # Create timeline for full PhD period
    ax.set_ylabel('Marathon Time (minutes)', fontsize=12, fontstyle='italic')
    ax.set_title('Marathon Performance (First Attempt Success)', fontsize=13, fontweight='normal')
    ax.grid(True, alpha=0.2)
    
    # Add threshold line at 4 hours (240 minutes)
    ax.axhline(y=240, color='black', linestyle='--', linewidth=0.5, alpha=0.5, label='4-hour threshold')
    
    # Create a continuous line showing "no data" as None until the marathon
    marathon_times = []
    dates = []
    
    for _, row in df.iterrows():
        dates.append(row['Date'])
        if row['Derek_Marathon_Time_minutes'] > 0:
            marathon_times.append(row['Derek_Marathon_Time_minutes'])
        else:
            marathon_times.append(None)
    
    # Plot Derek's marathon progression (flat line at None, then achievement)
    # We'll plot the full timeline with None values, then highlight the achievement
    derek_has_marathon = any(t is not None for t in marathon_times)
    
    if derek_has_marathon:
        # Find the index where marathon happened
        marathon_idx = next(i for i, t in enumerate(marathon_times) if t is not None)
        
        # Create line plot: y=0 before marathon, y=239 from marathon onwards
        # This creates a step function showing the achievement
        marathon_date = dates[marathon_idx]
        
        # Build the full timeline: 0 (or tiny value) before marathon, 239 after
        line_times = []
        for i in range(len(dates)):
            if i < marathon_idx:
                line_times.append(1)  # Nearly zero for visibility
            else:
                line_times.append(239)
        
        # Plot the continuous line showing the step up at marathon date
        ax.plot(dates, line_times, 'k-', linewidth=2.5, 
                label='Derek (sub-4hr)', zorder=5)
        
        # Add marker at the achievement point
        ax.plot(marathon_date, 239, 'ko', markersize=12, zorder=6)
        
        # Add vertical line to show when it happened
        ax.axvline(x=dates[marathon_idx], color='black', 
                   linestyle=':', linewidth=0.5, alpha=0.3)
        
        ax.set_ylim([0, 280])  # Rigorous y-axis starts at zero
        
        # Annotate the achievement - below the threshold and to the left
        ax.annotate('3h 59m\nOct 12, 2025\n(first attempt)', 
                    xy=(dates[marathon_idx], 239),
                    xytext=(-100, -50), textcoords='offset points',
                    fontsize=10, fontstyle='italic',
                    arrowprops=dict(arrowstyle='->', lw=0.5),
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=0.5))
        
        # Show "training period" before the marathon
        ax.text(dates[marathon_idx // 2], 50, 'Training period\n(pre-marathon)',
                fontsize=10, fontstyle='italic', ha='center',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=0.5))
        
        # Note Francesca's absence
        ax.text(0.02, 0.98, 'Francesca: No marathon attempts\n(priorities: 95 papers, 3564 citations)',
                transform=ax.transAxes, fontsize=9, fontstyle='italic',
                ha='left', va='top',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=0.5))
        
        ax.legend(loc='lower right', frameon=False, fontsize=11)
    else:
        ax.text(0.5, 0.5, 'No marathon data yet\n(training ongoing)',
                transform=ax.transAxes, fontsize=10, fontstyle='italic',
                ha='center', va='center')
        ax.set_ylim([0, 300])

def generate_report(df):
    """Generate statistical summary (rigorously objective)."""
    latest = df.iloc[-1]
    
    print("\n" + "="*80)
    print("LONGITUDINAL ACADEMIC METRICS ANALYSIS")
    print("Compiled by: Derek van Tilborg")
    print("Objectivity Level: Maximum")
    print("="*80 + "\n")
    
    print("HEIGHT ANALYSIS (PhD Period: Nov 2021 - Nov 2025)")
    print("-" * 40)
    derek_growth = latest['Derek_Height_cm'] - df['Derek_Height_cm'].iloc[0]
    francesca_change = latest['Francesca_Height_cm'] - df['Francesca_Height_cm'].iloc[0]
    print(f"Derek:     {latest['Derek_Height_cm']:.1f} cm (+{derek_growth:.1f} cm growth)")
    print(f"Francesca: {latest['Francesca_Height_cm']:.1f} cm ({francesca_change:.1f} cm settling)")
    print(f"Height Advantage: {latest['Derek_Height_cm'] - latest['Francesca_Height_cm']:.1f} cm")
    print()
    
    print("CITATION ANALYSIS (Raw, Misleading)")
    print("-" * 40)
    print(f"Derek:     {latest['Derek_Citations']:,} citations")
    print(f"Francesca: {latest['Francesca_Citations']:,} citations")
    print(f"Ratio:     Francesca has {latest['Francesca_Citations']/latest['Derek_Citations']:.2f}x more")
    print()
    
    print("HEIGHT-NORMALIZED PROWESS (van Tilborg Transform)")
    print("-" * 40)
    print(f"Derek:     {latest['Derek_Prowess']:.4f} efficiency score")
    print(f"Francesca: {latest['Francesca_Prowess']:.4f} efficiency score")
    
    if latest['Derek_Prowess'] > latest['Francesca_Prowess']:
        ratio = latest['Derek_Prowess'] / latest['Francesca_Prowess']
        print(f"Result:    Derek is {ratio:.2f}x more efficient ✓")
        print(f"           (Accounting for height penalty, growth bonus, log scaling)")
    else:
        ratio = latest['Francesca_Prowess'] / latest['Derek_Prowess']
        print(f"Result:    Francesca leads by {ratio:.2f}x")
        print(f"           (Further correction factors under development)")
    
    # Show simple metric for comparison
    print(f"\nSimple metric (flawed):")
    print(f"Derek:     {latest['Derek_Prowess_Simple']:.4f} citations/cm")
    print(f"Francesca: {latest['Francesca_Prowess_Simple']:.4f} citations/cm")
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
    
    print("Calculating height-normalized prowess metrics (van Tilborg Transform)...")
    df = calculate_height_normalized_prowess(df)
    
    print("Generating visualizations (Derek-approved aesthetic)...\n")
    
    # Create figure with subplots - share x-axis for temporal coherence
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True)
    fig.suptitle('Longitudinal Academic Performance Analysis: PhD Period (Nov 2021 - Nov 2025)\n(Rigorously Objective)', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    # Generate plots
    plot_height_trajectory(df, axes[0, 0])
    plot_citation_trajectory(df, axes[0, 1])
    plot_height_normalized_prowess(df, axes[1, 0])
    plot_marathon_achievement(df, axes[1, 1])
    
    # Format x-axis for all plots (shared, so only bottom row shows labels)
    for ax in axes.flat:
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.set_xlim([df['Date'].min(), df['Date'].max()])
    
    # Only show x-axis labels on bottom row
    for ax in axes[1, :]:
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
