from flet import *
import sqlite3

# Database setup
conn = sqlite3.connect("school.db", check_same_thread=False)
cursor = conn.cursor()

# Create Account table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Account(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        full_name TEXT,
        password TEXT,
        confirmation_password TEXT
    )
""")

# Create Student table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        math INTEGER,
        draw INTEGER,
        english INTEGER,
        arbic INTEGER,
        france INTEGER,
        chemistry INTEGER
    )
""")
conn.commit()

def main(page: Page):
    page.title = "School Management System"
    page.window.width = 400
    page.window.height = 800
    page.window.top = 1
    page.window.left = 900
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = "adaptive"
    page.bgcolor = "white"

    def malty_face(route):
        page.views.clear()
        
        # Home view
        page.views.append(
            View(
                "home",
                [ 
                    AppBar( 
                        title= Text("Abdalluh", size=25, width=350, text_align="center"),
                        color="white",
                        bgcolor="purple",
                    ),
                    Text("the home page \n\n", font_family="IBM Plex Sans Arabic", size=30, color='pink', width=400, text_align='center'),
                    Row([
                        Image(src="OIP (5).png", width=350, height=150, border_radius=2),
                    ], alignment=MainAxisAlignment.CENTER),
                    Text("welcome for you in our application \n\n", font_family="IBM Plex Sans Arabic", size=22, color='white', width=400, text_align='center', bgcolor=Colors.PURPLE_300),
                    Row([
                        ElevatedButton("Login", on_click=lambda _: page.go("login"), width=170, height=40, icon=Icons.LOGIN, style=ButtonStyle(
                            color="white",
                            bgcolor="purple"
                        )),
                        ElevatedButton("Create new account", on_click=lambda _: page.go("signup"), width=170, height=40, icon=Icons.PERSON_ADD, style=ButtonStyle(
                            color="white",
                            bgcolor="purple"
                        )),
                    ], alignment=MainAxisAlignment.CENTER)
                ]
            )
        )
        
        # Login view
        if page.route == "login":
            username_field = TextField(label="UserName", border_color='purple', width=400)
            email_field = TextField(label="E-mail", border_color='purple', width=400)
            password_field = TextField(label="Password", border_color='purple', width=400, password=True)
            
            def login_user(e):
                email = email_field.value
                password = password_field.value
                
                if not all([email, password]):
                    page.snack_bar = SnackBar(Text("Please fill all fields!"))
                    page.snack_bar.open = True
                    page.update()
                    return
                
                try:
                    # Check if user exists in database
                    cursor.execute("SELECT * FROM Account WHERE email = ? AND password = ?", (email, password))
                    user = cursor.fetchone()
                    
                    if user:
                        page.snack_bar = SnackBar(Text("Login successful!"))
                        page.snack_bar.open = True
                        page.update()
                        # Navigate to student management page
                        page.go("student_management")
                    else:
                        page.snack_bar = SnackBar(Text("Invalid email or password!"))
                        page.snack_bar.open = True
                        page.update()
                        
                except sqlite3.Error as e:
                    page.snack_bar = SnackBar(Text(f"Error: {str(e)}"))
                    page.snack_bar.open = True
                    page.update()
            
            page.views.append(
                View(
                    "login",
                    [
                        AppBar( 
                            title= Text("Login page", size=25, width=300, text_align='center'),
                            color="white",
                            bgcolor="purple",
                        ),
                        Text("the login page \n", font_family="IBM Plex Sans Arabic", size=30, color='black', width=400, text_align='center'),
                        username_field,
                        email_field,
                        password_field,
                        Row([
                            ElevatedButton("Login", on_click=login_user, width=170, height=40, icon=Icons.LOGIN, style=ButtonStyle(
                                color="white",
                                bgcolor="purple"
                            )),
                            ElevatedButton("New Account", on_click=lambda _: page.go("signup"), width=170, height=40, icon=Icons.PERSON_ADD, style=ButtonStyle(
                                color="white",
                                bgcolor="purple"
                            )),
                        ], alignment=MainAxisAlignment.CENTER)
                    ]
                )
            )
        
        # Signup view
        if page.route == "signup":
            email_field = TextField(label="E-mail", border_color='purple', width=400)
            full_name_field = TextField(label="Full Name", border_color='purple', width=400)
            password_field = TextField(label="Password", border_color='purple', width=400, password=True)
            confirm_password_field = TextField(label="Confirmation Password", border_color='purple', width=400, password=True)
            
            def add_account(e):
                email = email_field.value
                full_name = full_name_field.value
                password = password_field.value
                confirm_password = confirm_password_field.value
                
                if not all([email, full_name, password, confirm_password]):
                    page.snack_bar = SnackBar(Text("Please fill all fields!"))
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if password != confirm_password:
                    page.snack_bar = SnackBar(Text("Passwords don't match!"))
                    page.snack_bar.open = True
                    page.update()
                    return
                
                try:
                    cursor.execute("INSERT INTO Account (email, full_name, password, confirmation_password) VALUES (?, ?, ?, ?)", 
                                 (email, full_name, password, confirm_password))
                    conn.commit()
                    
                    page.snack_bar = SnackBar(Text("Account created successfully!"))
                    page.snack_bar.open = True
                    
                    email_field.value = ""
                    full_name_field.value = ""
                    password_field.value = ""
                    confirm_password_field.value = ""
                    
                    page.go("login")
                    
                except sqlite3.Error as e:
                    page.snack_bar = SnackBar(Text(f"Error: {str(e)}"))
                    page.snack_bar.open = True
                    page.update()
            
            page.views.append(
                View(
                    "signup",
                    [
                        AppBar( 
                            title= Text("Sign Up page", size=25, width=300, text_align='center'),
                            color="white",
                            bgcolor="purple",
                        ),
                        Text("Create Account", size=22, width=300, text_align='center', color='black'),
                        email_field,
                        full_name_field,
                        password_field,
                        confirm_password_field,
                        Row([
                            ElevatedButton("Create", on_click=add_account, width=170, height=40, icon=Icons.CREATE, style=ButtonStyle(
                                color="white",
                                bgcolor="purple"
                            )),
                            ElevatedButton("My Account", on_click=lambda _: page.go("login"), width=170, height=40, icon=Icons.ACCOUNT_BOX, style=ButtonStyle(
                                color="white",
                                bgcolor="purple"
                            )),
                        ], alignment=MainAxisAlignment.CENTER)
                    ]
                )
            )
        
        # Student Management view
        if page.route == "student_management":
            # Get student count
            table_name = "student"
            query = f"SELECT COUNT (*) FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchone()
            row_count = result[0]
            
            # Student fields
            name = TextField(label=" الاسم", icon=Icons.PERSON, height=35, rtl=True)
            email = TextField(label=" الايميل ", icon=Icons.MAIL, height=35, rtl=True)
            phone = TextField(label=" رقم  الهاتف", icon=Icons.PHONE, height=35, rtl=True)
            address = TextField(label=" العنوان ", icon=Icons.LOCATION_CITY, height=35, rtl=True)

            text = Text("درجات المواد  :", size=20, font_family="IBM Plex Sans Arabic", color="blue", rtl=True)
            math = TextField(label="الرياضبات ", width=100, height=35, rtl=True, color="black")
            arbic = TextField(label="عربي", width=100, height=35, rtl=True, color="black")
            english = TextField(label="انجليزي", width=100, height=35, rtl=True, color="black")
            france = TextField(label="الفرنسي", width=100, height=35, rtl=True, color="black")
            chemistry = TextField(label="العلوم", width=100, height=35, rtl=True, color="black")
            draw = TextField(label="الرسم", width=100, height=35, rtl=True, color="black")
            
            def add_student(e):
                try:
                    cursor.execute("INSERT INTO student (name, email, phone, address, math, draw, english, arbic, france, chemistry) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                                 (name.value, email.value, phone.value, address.value, math.value, draw.value, english.value, arbic.value, france.value, chemistry.value))
                    conn.commit()
                    
                    page.snack_bar = SnackBar(Text("Student added successfully!"))
                    page.snack_bar.open = True
                    
                    # Clear fields
                    name.value = ""
                    email.value = ""
                    phone.value = ""
                    address.value = ""
                    math.value = ""
                    draw.value = ""
                    english.value = ""
                    arbic.value = ""
                    france.value = ""
                    chemistry.value = ""
                    
                    # Update student count
                    page.go("student_management")
                    
                except sqlite3.Error as err:
                    page.snack_bar = SnackBar(Text(f"Error: {str(err)}"))
                    page.snack_bar.open = True
                    page.update()
            
            def show_students(e):
                cursor.execute("SELECT * FROM student")
                fetch_data = cursor.fetchall()
                
                # Create a dialog to show students
                students_list = Column(scroll="adaptive")
                for student in fetch_data:
                    students_list.controls.append(
                        Text(f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}", size=12)
                    )
                
                def close_dialog(e):
                    page.dialog.open = False
                    page.update()
                
                page.dialog = AlertDialog(
                    title=Text("Students List"),
                    content=students_list,
                    actions=[TextButton("Close", on_click=close_dialog)]
                )
                page.dialog.open = True
                page.update()
            
            def logout(e):
                page.go("home")
            
            add_button = ElevatedButton(
                "حفض البيانات", 
                width=120, 
                icon=Icons.SAVE,
                style=ButtonStyle(color="black", bgcolor="blue", padding=15),
                on_click=add_student
            )
            
            show_button = ElevatedButton(
                "عرض الطلاب", 
                width=120, 
                icon=Icons.LIST,
                style=ButtonStyle(color="black", bgcolor="green", padding=15),
                on_click=show_students
            )
            
            logout_button = ElevatedButton(
                "Logout", 
                width=120, 
                icon=Icons.LOGOUT,
                style=ButtonStyle(color="white", bgcolor="red", padding=15),
                on_click=logout
            )
            
            page.views.append(
                View(
                    "student_management",
                    [
                        AppBar( 
                            title= Text("Student Management", size=25, width=350, text_align="center"),
                            color="white",
                            bgcolor="blue",
                        ),
                        Row([
                            Image(src="image_processing.jpg", width=200)
                        ], alignment=MainAxisAlignment.CENTER),
                        
                        Row([
                            Text(" ادارت الطلاب ", size=30, font_family="IBM Plex Sans Arabic", color="black")
                        ], alignment=MainAxisAlignment.CENTER),
                        
                        Row([
                            Text("عدد الطلاب : ", size=20, font_family="IBM Plex Sans Arabic", color="red"),
                            Text(row_count, size=20, font_family="IBM Plex Sans Arabic", color="red")
                        ], alignment=MainAxisAlignment.CENTER),
                        
                        name, email, phone, address, text,
                        
                        Row([math, draw, english], alignment=MainAxisAlignment.CENTER),
                        
                        Row([arbic, france, chemistry], alignment=MainAxisAlignment.CENTER),
                        
                        Row([add_button, show_button, logout_button], alignment=MainAxisAlignment.CENTER)
                    ]
                )
            )
        
        page.update()

    def back_page(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
    
    page.on_route_change = malty_face
    page.on_view_pop = back_page
    page.go(page.route)

app(main)