import pandas as pd
from models import db
from models.ski_resort import SkiResort
from app import app


def clean_price(value):
    if pd.isna(value) or str(value).strip().lower() in ['free', 'nan']:
        return 0.0
    try:
        return float(value)
    except:
        return 0.0

def import_data(path):
    df = pd.read_csv(path)
    
    # Convert relevant columns
    df['lift_ticket_price_weekday_usd'] = df['lift_ticket_price_weekday_usd'].apply(clean_price)
    df['lift_ticket_price_weekend_usd'] = df['lift_ticket_price_weekend_usd'].apply(clean_price)
    
    # Replace the existing pass_type handling with:
    df['pass_type'] = df['pass_type'].fillna('None').str.strip()
    
    # Convert other numeric columns
    numeric_cols = ['difficulty_beginner_pct', 'difficulty_intermediate_pct', 
                   'difficulty_advanced_pct', 'annual_snowfall_inches',
                   'skiable_acres', 'vertical_drop_ft']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Convert boolean column
    #print(df['allow_snowboard'].unique())
    df['allow_snowboard'] = df['allow_snowboard'].str.strip().str.lower() == 'yes'
    
    # Insert data
    with app.app_context():
        db.drop_all()   # Optional: Wipe clean if re-importing
        db.create_all()
        for _, row in df.iterrows():
            resort = SkiResort(
                resort_name=row['resort_name'],
                state=row['state'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                lift_ticket_price_weekday_usd=row['lift_ticket_price_weekday_usd'],
                lift_ticket_price_weekend_usd=row['lift_ticket_price_weekend_usd'],
                difficulty_beginner_pct=row['difficulty_beginner_pct'],
                difficulty_intermediate_pct=row['difficulty_intermediate_pct'],
                difficulty_advanced_pct=row['difficulty_advanced_pct'],
                busiest_days=row['busiest_days'],
                annual_snowfall_inches=row['annual_snowfall_inches'],
                skiable_acres=row['skiable_acres'],
                vertical_drop_ft=row['vertical_drop_ft'],
                pass_type=row['pass_type'],
                allow_snowboard=row['allow_snowboard']
            )
            db.session.add(resort)
        
        db.session.commit()

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    import_data(path)
    