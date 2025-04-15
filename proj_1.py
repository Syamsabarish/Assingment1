import streamlit as st
import sqlite3
import pandas as pd

#Functions
def execute_query(query, params=()):
    conn = sqlite3.connect('food_wastage.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_data(table_name):
    conn = sqlite3.connect('food_wastage.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    return pd.DataFrame(data, columns=columns)

def run_sql_query(query, params=()):
    conn = sqlite3.connect('food_wastage.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.close()
    return pd.DataFrame(results, columns=column_names)

# ----------------- Pages Starts here-----------------

#--------------------Home Page------------------------
def home_page():
    st.title("🍽️ Local Food Wastage Management System 🌍")
    image_url = 'https://th.bing.com/th/id/R.e45406a9629df477df8e67c9f6918dfa?rik=ba9ss%2fztkYeZIA&riu=http%3a%2f%2fbsdgroup.ca%2fblog%2fwp-content%2fuploads%2f2020%2f10%2fReducing-Food-Waste-scaled.jpg&ehk=gs7mG7M2fJcKXgwfTQsyzENWBMWHMB%2fu8inTBzm6CGw%3d&risl=&pid=ImgRaw&r=0'
     # Use HTML to center the image and control size
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="{image_url}" width="500" alt="Food Wastage Image"/>
            <p style="font-style: italic;">Together, let's reduce food wastage and make a difference!</p>
        </div>
    """,True)
    
    st.markdown("""
                ### Objective🤝           
                The Local Food Wastage Management System♻️ \n  \t  👉 An innovative platform aimed at tackling food wastage by connecting food providers (such as restaurants, grocery stores, etc.) with receivers (such as individuals, NGOs,Charity,etc) to distribute surplus food. """
                )

#--------------------Page 1(Tables Viewer) ------------------------
def page_1():
    st.title("📊 Explore Data Tables")

    options = {
        'Providers Data': 'providers',
        'Receivers Data': 'receivers',
        'Claims Data': 'claims',
        'Food Listings Data': 'food'
    }

    selected_option = st.selectbox('Choose a table to explore:', list(options.keys()))
    table_name = options[selected_option]

    try:
        df = fetch_data(table_name)
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning(f"No data found in the `{table_name}` table.")
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")

#--------------------Page 2(CRUD) ------------------------
# Create Provider
def create_provider():
    with st.form("provider_form"):
        name = st.text_input("Name")
        type = st.text_input("Type")
        address = st.text_input("Address")
        city = st.text_input("City")
        contact = st.text_input("Contact Info")
        submitted = st.form_submit_button("Submit")
        if submitted:
            execute_query(
                "INSERT INTO providers (Name,Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?)",
                (name, type, address, city, contact)
            )
            st.success("✅ Provider added successfully!")

# Create Receiver
def create_receiver():
    with st.form("receiver_form"):
        name = st.text_input("Name")
        Type = st.text_input("Type")
        contact = st.text_input("Contact Info")
        city = st.text_input("City")
        submitted = st.form_submit_button("Submit")
        if submitted:
            execute_query(
                "INSERT INTO receivers (Name, Type, Contact, City) VALUES (?, ?, ?,?)",
                (name,Type,contact,city)
            )
            st.success("✅ Receiver added successfully!")

# Create Claim
def create_claim():
    with st.form("claim_form"):
        Claim_ID = st.text_input("Claim ID")
        Food_ID = st.text_input("Food ID")  # Added this missing input
        Receiver_ID = st.text_input("Receiver ID")
        status = st.selectbox("Status", ["Pending", "Completed", "Canceled"])
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            execute_query(
                """
                INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
                VALUES (?, ?, ?, ?, DATETIME('now'))
                """,
                (Claim_ID, Food_ID, Receiver_ID, status)
            )
            st.success("✅ Claim added successfully with current timestamp!")

def create_food_listing():
    with st.form("food_listing_form"):
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1)
        expiry_date = st.date_input("Expiry Date")
        provider_id = st.number_input("Provider ID", min_value=1)

        # Dropdown for Provider Type
        provider_type = st.selectbox("Provider Type", [
            "Catering Service", 
            "Grocery Store", 
            "Restaurant", 
            "Supermarket"
        ])

        location = st.text_input("Location")

        # Dropdown for Food Type
        food_type = st.selectbox("Food Type", [
            "Non-Vegetarian",
            "Vegan",
            "Vegetarian"
        ])

        # Dropdown for Meal Type
        meal_type = st.selectbox("Meal Type", [
            "Breakfast",
            "Lunch",
            "Dinner"
        ])

        submitted = st.form_submit_button("Submit")
        if submitted:
            execute_query(
                """
                INSERT INTO food (
                    Food_Name, Quantity, Expiry_Date,provider_id,
                    Provider_Type, Location,
                    Food_Type, Meal_Type
                ) VALUES (?, ?, ?, ?, ?, ?, ?,?)
                """,
                ( food_name, quantity, expiry_date,
                 provider_id, provider_type, location,
                 food_type, meal_type)
            )
            st.success("✅ Food listing added successfully!")



# Read Data
def read_data(table_name):
    try:
        df = fetch_data(table_name)
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning(f"No data found in `{table_name}`.")
    except Exception as e:
        st.error(f"❌ Error reading data: {e}")

def update_provider():
    with st.form("update_provider_form"):
        Old_provider_name = st.text_input("Old Provider Name")
        name = st.text_input("New Name")
        provider_type = st.text_input("New Provider Type")
        address = st.text_input("New Address")
        city = st.text_input("New City")
        contact = st.text_input("New Contact Info")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            try:
                execute_query(
                    """UPDATE providers 
                       SET Name = ?, Type = ?, Address = ?, City = ?, Contact = ? 
                       WHERE Name = ?""",
                    (name, provider_type, address, city, contact, Old_provider_name)
                )
                st.success("✅ Provider updated successfully!")
            except Exception as e:
                st.error(f"❌ Update failed: {e}")


def update_receiver():
    with st.form("update_receiver_form"):
        receiver_id = st.number_input("Receiver ID to Update", min_value=1)
        name = st.text_input("New Name")
        receiver_type = st.text_input("Receiver Type")
        contact = st.text_input("New Contact Info")
        city = st.text_input("New City")

        submitted = st.form_submit_button("Submit")
        if submitted:
            try:
                execute_query(
                    """UPDATE receivers 
                       SET Name = ?, Type = ?, Contact = ?, City = ?
                       WHERE Receiver_ID = ?""",
                    (name, receiver_type, contact, city, receiver_id)
                )
                st.success(f"✅ Receiver with ID {receiver_id} updated successfully!")
            except Exception as e:
                st.error(f"❌ Failed to update: {e}")

          

# Update Claim (Status + Timestamp)
def update_claim():
    with st.form("update_claim_form"):
        claim_id = st.number_input("Claim ID to Update", min_value=1)
        status = st.selectbox("New Status", ["Pending", "Completed", "Canceled"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            execute_query(
                """
                UPDATE claims 
                SET Status = ?, Timestamp = DATETIME('now') 
                WHERE Claim_ID = ?
                """,
                (status, claim_id)
            )
            st.success("✅ Claim updated successfully with current timestamp!")


# Update Food Listing
def update_food_listing():
    with st.form("update_food_listing_form"):
        food_id = st.number_input("Food Listing ID to Update", min_value=1)
        food_Name= st.text_input("New Food Item")
        quantity = st.number_input("New Quantity", min_value=1)
        expiry_date = st.date_input("New Expiry Date")
        submitted = st.form_submit_button("Submit")
        if submitted:
            execute_query(
                """UPDATE food 
                   SET Food_Name = ?, Quantity = ?, Expiry_Date = ? 
                   WHERE Food_ID = ?""",
                (food_Name, quantity, expiry_date, food_id)
            )
            st.success("✅ Food listing updated successfully!")

# Delete Provider
def delete_provider():
    provider_id = st.text_input("Provider Name to Delete")
    if st.button("Delete Provider"):
        execute_query(
            "DELETE FROM providers WHERE Name = ?",
            (provider_id,)
        )
        st.success(f"✅ Provider with ID {provider_id} deleted successfully!")

# Delete Receiver
def delete_receiver():
    Name = st.text_input("Receiver Name to Delete")
    if st.button("Delete Receiver"):
        execute_query(
            "DELETE FROM receivers WHERE Name = ?", (Name,)
        )
        st.success(f"✅ Receiver with Name {Name} deleted successfully!")

# Delete Claim
def delete_claim():
    claim_id = st.number_input("Claim ID to Delete", min_value=1)
    if st.button("Delete Claim"):
        execute_query(
            "DELETE FROM claims WHERE Claim_ID = ?",
            (claim_id,)
        )
        st.success(f"✅ Claim with ID {claim_id} deleted successfully!")

# Delete Food Listing
def delete_food_listing():
    food_id = st.number_input("Food Listing ID to Delete", min_value=1)
    if st.button("Delete Food Listing"):
        execute_query(
            "DELETE FROM food WHERE Food_ID = ?",
            (food_id,)
        )
        st.success(f"✅ Food listing with ID {food_id} deleted successfully!")

# --- Main Streamlit Interface ---
def page_2():
    st.title("🛠️ Manage Data (CRUD)")

    table_name = st.selectbox('Choose a table to modify:', ['providers', 'receivers', 'claims', 'food'])
    operation = st.selectbox('Choose an operation:', ['Create', 'Read', 'Update', 'Delete'])

    if operation == 'Create':
        if table_name == 'providers':
            create_provider()
        elif table_name == 'receivers':
            create_receiver()
        elif table_name == 'claims':
            create_claim()
        elif table_name == 'food':
            create_food_listing()

    elif operation == 'Read':
        read_data(table_name)

    elif operation == 'Update':
        if table_name == 'providers':
            update_provider()
        elif table_name == 'receivers':
            update_receiver()
        elif table_name == 'claims':
            update_claim()
        elif table_name == 'food':
            update_food_listing()

    elif operation == 'Delete':
        if table_name == 'providers':
            delete_provider()
        elif table_name == 'receivers':
            delete_receiver()
        elif table_name == 'claims':
            delete_claim()
        elif table_name == 'food':
            delete_food_listing()
    
#--------------------Page 3(SQL Explorer) ------------------------
def page_3():
    st.title("📈 SQL Query Explorer")

    questions = {
        "How many food providers and receivers are there in each city?":
            "SELECT City, COUNT(*) as Total_Providers FROM providers GROUP BY City",

        "Which type of food provider contributes the most food?":
            "SELECT Type, COUNT(*) as Contributions FROM providers GROUP BY Type ORDER BY Contributions DESC",

        "Contact info of providers in a city":
            "SELECT Name, Contact FROM providers WHERE City LIKE ?",

        "Receivers with most food claims":
            "SELECT c.Receiver_ID,r.Name,COUNT(*) as Total_Claims FROM claims c JOIN receivers r ON r.Receiver_ID = c.Receiver_ID GROUP BY c.Receiver_ID ORDER BY Total_Claims DESC ",

        "Total quantity of food available":
            "SELECT SUM(Quantity) as Total_Quantity FROM food",

        "City with highest food listings":
            "SELECT Location AS city,COUNT(*) AS num_food_listings FROM food GROUP BY city ORDER BY num_food_listings DESC LIMIT 1 ",

        "Most common food types":
            "SELECT Food_Type, COUNT(*) as Count FROM food GROUP BY Food_Type ORDER BY Count DESC",

        "Food listings expiring in next 3 days":
            "SELECT c.Claim_ID,f.Food_Name, r.Name AS Receiver_Name, c.Status, c.Timestamp FROM claims c JOIN food f ON c.Food_ID = f.Food_ID JOIN receivers r ON c.Receiver_ID = r.Receiver_ID WHERE c.Timestamp >= DATE('now', '-3 day') ORDER BY c.Timestamp DESC",

        "Claims made per food item":
            "SELECT f.Food_Name, COUNT(*) AS claim_count FROM claims c INNER JOIN food f ON c.Food_ID = f.Food_ID WHERE c.Status = 'Completed' GROUP BY f.Food_ID ORDER BY claim_count DESC",

        "Provider with most successful claims":
            "SELECT f.Food_ID,f.Food_Name,p.Name AS Provider_Name,COUNT(*) OVER (PARTITION BY p.Name) AS successful_claims FROM providers p  INNER JOIN food f ON p.Provider_ID = f.Provider_ID  INNER JOIN claims c ON c.Food_ID = f.Food_ID WHERE c.Status = 'Completed' ORDER BY successful_claims DESC LIMIT 1;",

        "City with fastest claim rate":
            "SELECT p.City,COUNT(*) AS completed_claims FROM claims c JOIN food f ON c.Food_ID = f.Food_ID JOIN providers p ON f.Provider_ID = p.Provider_ID WHERE c.Status = 'Completed' GROUP BY p.City ORDER BY completed_claims DESC limit 5",

        "Claim status percentages":
            "SELECT Status, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage FROM claims GROUP BY Status",

        " Average quantity of food claimed per receiver":
            "SELECT c.Receiver_ID,ROUND(AVG(f.Quantity), 2) AS avg_claimed_quantity FROM claims c JOIN food f ON c.Food_ID = f.Food_ID WHERE c.Status = 'Completed' GROUP BY c.Receiver_ID ORDER BY avg_claimed_quantity DESC",
    
        "Total quantity of food donated by each provider":      
            " SELECT p.Provider_ID,p.Name,SUM(f.Quantity) AS total_donated FROM providers p JOIN food  f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY total_donated DESC",
        
        "Which meal type (breakfast, lunch, dinner, snacks) is claimed the most":
            "SELECT f.Meal_Type,COUNT(*) AS total_claims FROM claims c JOIN food f ON c.Food_ID = f.Food_ID WHERE c.Status = 'Completed' GROUP BY f.Meal_Type  ORDER BY total_claims DESC limit 1"
        }

    question = st.selectbox("💡 Choose a question to explore:", list(questions.keys()))

    if "Contact info" in question:
        city = st.text_input("🔍 Enter city name:")
        if city:
            df = run_sql_query(questions[question], (f"%{city}%",))
            st.dataframe(df)
    else:
        df = run_sql_query(questions[question])
        st.dataframe(df)   
#----------------------page 4 (Additional SQL Query Explorer)----------------
def page_4():
    st.title("Additional SQL Query Explorer")

    questions = {
        "Find all food items that have not been claimed yet ":
            "SELECT f.Food_Name, f.Quantity FROM Food  f LEFT JOIN Claims c ON f.Food_ID = c.Food_ID WHERE c.Claim_ID ISNULL GROUP BY f.Food_Name ",
    
        "Providers who have offered food items that have been claimed by receivers who are NGOs ":
            "SELECT DISTINCT p.Provider_ID, p.Name AS Provider_Name, p.City FROM providers p JOIN food f ON p.Provider_ID = f.Provider_ID JOIN claims c ON f.Food_ID = c.Food_ID JOIN receivers r ON c.Receiver_ID = r.Receiver_ID WHERE r.Type = 'NGO' AND c.Status = 'Completed' ",
       
        "Cities Where Claims Are Frequently Cancelled":
            "SELECT r.City,COUNT(*) AS Cancelled_Claims FROM claims c JOIN receivers r ON c.Receiver_ID = r.Receiver_ID WHERE c.Status = 'Cancelled' GROUP BY r.City ORDER BY Cancelled_Claims DESC ",
        
        " Food Items That Were Listed But Never Claimed":
            "SELECT f.Food_ID,f.Food_Name FROM food f LEFT JOIN claims c ON f.Food_ID = c.Food_ID WHERE c.Food_ID IS NULL",
        
        "Distribution of Food Types per City":
            "SELECT f.Location AS City,f.Food_Type, COUNT(*) AS Count FROM food f GROUP BY f.Location, f.Food_Type ORDER BY City, Count DESC "
        }

    question = st.selectbox("✨ Select a query to run:", list(questions.keys()))
    df = run_sql_query(questions[question])
    st.dataframe(df)
# ----------------- Main Layout -----------------
def main():
    st.set_page_config(page_title="Food Wastage Management", layout="wide")

    st.sidebar.title("🌐 Navigation")
    st.sidebar.markdown("Manage food, providers & more 🚀")
    st.sidebar.markdown("---")
    app_mode = st.sidebar.radio("📌 Go to:", [
        "🏠 Home Dashboard",
        "📊 Explore Data Tables",
        "🛠️ CRUD Operations",
        "📈 SQL Query Explorer",
        "🔍 Additional Query Explorer"
    ])
    st.sidebar.markdown("---")
    
    if app_mode == "🏠 Home Dashboard":
        home_page()
    elif app_mode == "📊 Explore Data Tables":
        page_1()
    elif app_mode == "🛠️ CRUD Operations":
        page_2()
    elif app_mode == "📈 SQL Query Explorer":
        page_3()
    elif app_mode =="🔍 Additional Query Explorer":
        page_4()
if __name__ == "__main__":
    main()
