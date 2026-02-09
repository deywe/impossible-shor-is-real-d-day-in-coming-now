import matplotlib
import warnings
import matplotlib
matplotlib.use('Qt5Agg') # Força o uso do motor que instalamos
# Silencing font/glyph warnings for a clean terminal output
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

try:
    matplotlib.use('Qt5Agg') 
except:
    matplotlib.use('TkAgg') 

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
import os

CSV_FILE = "1qubit_cracks_rsa_for_ever.csv"

def start_player():
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: '{CSV_FILE}' not found.")
        return

    print(f"📂 Loading {CSV_FILE}...")
    # Loading with full precision
    df = pd.read_csv(CSV_FILE)
    
    x_columns = [c for c in df.columns if c.endswith('_x') and c.startswith('q')]
    n_qubits = len(x_columns)
    total_frames = len(df)
    
    print(f"📼 Tape Loaded: {total_frames} frames | {n_qubits} Qubits")

    max_x = df[x_columns].abs().max().max()
    z_columns = [c.replace('_x', '_z') for c in x_columns]
    # Capturing real amplitude
    max_z = df[z_columns].abs().max().max()
    
    # --- SOVEREIGN GOLD ADJUSTMENT ---
    # Calculating the ratio with 64-bit float precision
    real_factor = np.float64(max_z) / np.float64(max_x) if max_x > 0 else 0
    
    print(f"📏 Geometry -> Radius: {max_x:.2f} | Height: {max_z:.8f}")
    print(f"🥯 Real Flattening Factor: {real_factor:.8f}")

    fig = plt.figure(figsize=(14, 9), facecolor='#050505')
    ax = fig.add_subplot(111, projection='3d', facecolor='#050505')
    
    # Forcing box_aspect so Z remains visible even if extremely thin
    ax.set_box_aspect([1, 1, 0.4]) 
    
    ax.set_xlim(-max_x, max_x)
    ax.set_ylim(-max_x, max_x)
    
    # VISUAL FLOOR: Setting a render limit to prevent the 'leaf' from vanishing
    z_render_limit = max(max_z * 10, 0.0001)
    ax.set_zlim(-z_render_limit, z_render_limit) 
    ax.axis('off')

    colors = plt.cm.hsv(np.linspace(0, 1, n_qubits))
    
    # lw=0.5 for sharp and elegant high-qubit rendering
    lines = [ax.plot([], [], [], color=colors[i], lw=1.7, alpha=0.8)[0] for i in range(n_qubits)]
    
    txt_frame = ax.text2D(0.02, 0.95, ">> HARPIA SOVEREIGN GOLD", transform=ax.transAxes, color='#ffd700', fontsize=12, fontweight='bold')
    txt_info = ax.text2D(0.02, 0.90, "", transform=ax.transAxes, color='#00ffcc', fontsize=10)

    def update(frame_idx):
        idx = frame_idx % total_frames
        row = df.iloc[idx]
        
        # Optimization: Trace tail of 20 frames for Gold mode
        start = max(0, idx - 20)
        slice_df = df.iloc[start : idx+1]
        
        for i in range(n_qubits):
            lines[i].set_data(slice_df[f'q{i}_x'], slice_df[f'q{i}_y'])
            lines[i].set_3d_properties(slice_df[f'q{i}_z'])

        txt_frame.set_text(f"FRAME: {idx}/{total_frames} | PHOENIX STABILIZED")
        # Displaying with 8 decimal places
        txt_info.set_text(f"Z-Amplitude: {row['q0_z']:.8f}\nSPHY Factor: {real_factor:.8f}")
        
        # Sovereign Dynamic Camera: Oscillates to showcase the membrane depth
        ax.view_init(elev=12 + np.sin(idx/100)*4, azim=idx*0.3)
        
        return lines + [txt_frame, txt_info]

    # Cinematic interval of 15ms for maximum fluidity
    anim = FuncAnimation(fig, update, frames=total_frames, interval=15, blit=False)
    
    print("🚀 Sovereign Gold Visualizer Ignited... Observe the membrane!")
    plt.show()

if __name__ == "__main__":
    start_player()