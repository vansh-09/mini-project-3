import os
from PIL import Image, ImageDraw

OUTPUT_DIR = "sample_diagrams"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_sample_1(path=os.path.join(OUTPUT_DIR, "sample_diagram_1.png")):
    ensure_output_dir()
    img = Image.new('RGB', (800, 500), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((250, 20), "Global Temperature Anomaly (1980 - 2020)", fill=(0, 0, 0))
    
    # Axes
    draw.line([(100, 400), (700, 400)], fill=(0, 0, 0), width=3) # X-axis
    draw.line([(100, 400), (100, 100)], fill=(0, 0, 0), width=3) # Y-axis
    
    # Axis labels
    draw.text((370, 440), "Year", fill=(0, 0, 0))
    draw.text((15, 240), "Temp (°C)", fill=(0, 0, 0))
    
    # Grid & Ticks
    years = ["1980", "1990", "2000", "2010", "2020"]
    for i, y in enumerate(years):
        x = 100 + i * 150
        draw.line([(x, 400), (x, 405)], fill=(0, 0, 0), width=2)
        draw.text((x - 15, 412), y, fill=(50, 50, 50))
        
    temps = ["0.0", "0.3", "0.6", "0.9", "1.2"]
    for i, t in enumerate(temps):
        y = 400 - i * 70
        draw.line([(95, y), (100, y)], fill=(0, 0, 0), width=2)
        draw.text((60, y - 5), t, fill=(50, 50, 50))
        
    # Data line
    points = [(100, 390), (250, 340), (400, 280), (550, 210), (700, 120)]
    draw.line(points, fill=(220, 40, 40), width=4)
    for p in points:
        draw.ellipse([p[0]-5, p[1]-5, p[0]+5, p[1]+5], fill=(180, 0, 0))
        
    # Annotation/Legend
    draw.rectangle([(520, 100), (680, 140)], outline=(100, 100, 100), width=1)
    draw.line([(530, 120), (560, 120)], fill=(220, 40, 40), width=3)
    draw.text((570, 113), "Temp Rise", fill=(0, 0, 0))

    img.save(path)
    print(f"Saved {path}")

def create_sample_2(path=os.path.join(OUTPUT_DIR, "sample_diagram_2.png")):
    ensure_output_dir()
    img = Image.new('RGB', (800, 500), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((280, 20), "Photosynthesis Process Overview", fill=(0, 0, 0))
    
    # Sun Box
    draw.rectangle([(50, 80), (200, 160)], fill=(255, 235, 150), outline=(230, 180, 0), width=2)
    draw.text((80, 110), "Sunlight (Energy)", fill=(100, 70, 0))
    
    # CO2 + H2O Box
    draw.rectangle([(50, 280), (200, 360)], fill=(200, 230, 255), outline=(50, 120, 200), width=2)
    draw.text((70, 310), "Carbon Dioxide\n+ Water (H2O)", fill=(0, 50, 120))
    
    # Central Leaf / Reactor Box
    draw.rectangle([(320, 150), (500, 290)], fill=(200, 245, 200), outline=(40, 160, 40), width=3)
    draw.text((360, 200), "LEAF (Chloroplast)\n\n6CO2 + 6H2O\n--> C6H12O6 + 6O2", fill=(10, 80, 10))
    
    # Arrows In
    draw.line([(200, 120), (320, 180)], fill=(200, 150, 0), width=3)
    draw.line([(200, 320), (320, 250)], fill=(30, 100, 180), width=3)
    
    # Outputs Box
    draw.rectangle([(600, 150), (760, 290)], fill=(255, 220, 220), outline=(200, 50, 50), width=2)
    draw.text((620, 190), "OUTPUTS:\n- Oxygen (O2)\n- Glucose (Sugar)", fill=(120, 10, 10))
    
    # Arrow Out
    draw.line([(500, 220), (600, 220)], fill=(40, 160, 40), width=3)

    img.save(path)
    print(f"Saved {path}")

def create_sample_3(path=os.path.join(OUTPUT_DIR, "sample_diagram_3.png")):
    ensure_output_dir()
    img = Image.new('RGB', (800, 500), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((260, 20), "Renewable vs Non-Renewable Energy (2024)", fill=(0, 0, 0))
    
    categories = ["Solar", "Wind", "Hydro", "Coal"]
    values = [35, 25, 20, 45]
    colors = [(255, 180, 0), (100, 200, 255), (50, 150, 255), (120, 120, 120)]
    
    # Axes
    draw.line([(100, 400), (700, 400)], fill=(0, 0, 0), width=2)
    draw.line([(100, 400), (100, 100)], fill=(0, 0, 0), width=2)
    
    for i, (cat, val, col) in enumerate(zip(categories, values, colors)):
        x_left = 140 + i * 140
        x_right = x_left + 80
        bar_height = val * 6
        y_top = 400 - bar_height
        
        draw.rectangle([(x_left, y_top), (x_right, 400)], fill=col, outline=(0, 0, 0))
        draw.text((x_left + 20, 415), cat, fill=(0, 0, 0))
        draw.text((x_left + 25, y_top - 20), f"{val}%", fill=(0, 0, 0))

    img.save(path)
    print(f"Saved {path}")

if __name__ == "__main__":
    create_sample_1()
    create_sample_2()
    create_sample_3()
