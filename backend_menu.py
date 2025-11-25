from storage import SystemDB

db_conn = SystemDB()

class MenuCreation:
    def __init__(self):
        pass

    # Adding Meal
    def add_meal(self, name, description, price,  cuisineID, courseID,Status=True, prepTime=0):
        try:
            db_conn.cursor.execute("SELECT id FROM Meals WHERE name = %s", (name,))
            if db_conn.cursor.fetchone():
                return f"Error: {name} already exists."

            db_conn.cursor.execute(
                """INSERT INTO Meals 
                (name, description, price, Status, prepTime, cuisineID, courseID)  
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (name, description, price, Status, prepTime, cuisineID, courseID)
            )

            db_conn.connection.commit()
            return "Meal added successfully"
        except Exception as e:
            return f"Error adding meal: {e}"
        
    # Display Meals (with filters)
    def display(self, cuisine_id=None, course_id=None):
            query = """
                SELECT 
                    m.id, m.name, m.description, m.price, m.Status,
                    m.prepTime, c.name AS cuisine, co.name AS course
                FROM Meals m
                LEFT JOIN Cuisines c ON m.cuisineID = c.id
                LEFT JOIN Courses co ON m.courseID = co.id
            """
            params = ()
            if cuisine_id is not None and course_id is not None:
                query += " WHERE m.cuisineID = %s AND m.courseID = %s"
                params = (cuisine_id, course_id)

            elif cuisine_id is not None:
                query += " WHERE m.cuisineID = %s"
                params = (cuisine_id,)

            elif course_id is not None:
                query += " WHERE m.courseID = %s"
                params = (course_id,)

            db_conn.cursor.execute(query, params)
            return db_conn.cursor.fetchall()

        

    # Update Meal
    def update(self, meal_id, price=None, status=None):
        try:
            updated = False
            if price is not None:
                db_conn.cursor.execute("UPDATE Meals SET price = %s WHERE id = %s", (price, meal_id))
                if db_conn.cursor.rowcount > 0:
                    updated = True
            if status is not None:
                db_conn.cursor.execute("UPDATE Meals SET status = %s WHERE id = %s", (status, meal_id))
                if db_conn.cursor.rowcount > 0:
                    updated = True

            db_conn.connection.commit()

            if updated:
                return "Meal successfully updated"
            else:
                return "No changes made, check meal ID"
        except Exception as e:
            return f"Error updating meal: {e}"


    # Delete Meal
    def delete(self, id):
        try:
            db_conn.cursor.execute("DELETE FROM Meals WHERE id = %s", (id,))
            db_conn.connection.commit()

            db_conn.cursor.execute("SELECT COUNT(*) FROM Meals")
            count = db_conn.cursor.fetchone()[0]

        # If empty, reset auto-increment
            if count == 0:
                db_conn.cursor.execute("ALTER TABLE Meals AUTO_INCREMENT = 1")
                db_conn.connection.commit()

            return "Meal deleted successfully!"
        except:
            return f"Error deleting meal"

    def fetch_all(self, table_name):
        try:
            db_conn.cursor.execute(f"SELECT id, name FROM {table_name}")
            return db_conn.cursor.fetchall()
        except Exception as e:
            return f"Error fetching {table_name}: {e}"

    def get_categories(self):
        return self.fetch_all("Courses")

    def get_cuisines(self):
        return self.fetch_all("Cuisines")

