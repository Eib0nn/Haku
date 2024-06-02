import tkinter
import customtkinter
from PIL import Image
import os
import json
from crop_calc import Crops_calculator as calc

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window configuration
        self.title("ALL I CAN FEEL IS PAIN")
        self.geometry(f"{1130}x{700}")  # Increased height for better layout

        # load images path
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "Parsnip.png")), size=(45, 45))

        # 5x5 grid config
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure((2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 4), weight=1)

        # sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=210, corner_radius=0, fg_color="red")
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # crop_option scrollable container
        self.crop_option_container = customtkinter.CTkFrame(self, corner_radius=10)
        self.crop_option_container.grid(row=0, column=1, sticky="nsew", columnspan=2, padx=10, pady=10)
        self.crop_option_container.grid_rowconfigure(0, weight=1)
        self.crop_option_container.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.crop_option_canvas = tkinter.Canvas(self.crop_option_container, bg="#242424", highlightthickness=0)
        self.crop_option_canvas.grid(row=0, column=0, sticky="nsew", columnspan=5)

        self.crop_option_scrollbar = customtkinter.CTkScrollbar(self.crop_option_container, orientation="vertical", command=self.crop_option_canvas.yview, corner_radius=10)
        self.crop_option_scrollbar.grid(row=0, column=6, sticky="ns")

        self.crop_option_canvas.configure(yscrollcommand=self.crop_option_scrollbar.set)

        self.crop_option_frame = customtkinter.CTkFrame(self.crop_option_canvas, corner_radius=10, fg_color="#A32DC4")
        self.crop_option_canvas.create_window((0, 0), window=self.crop_option_frame, anchor="nw")
        self.crop_option_frame.bind("<Configure>", lambda e: self.crop_option_canvas.configure(scrollregion=self.crop_option_canvas.bbox("all")))

        # Adjusting columns to spread buttons more
        for col in range(4):  # Assuming we want to use 4 columns
            self.crop_option_frame.grid_columnconfigure(col, weight=1)

        # Scrollable frame setup for calculator frames
        self.scrollable_frame_container = customtkinter.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.scrollable_frame_container.grid(row=1, column=1, sticky="nsew", columnspan=2, padx=10, pady=30)
        self.scrollable_frame_container.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_container.grid_rowconfigure(0, weight=1)

        self.canvas = tkinter.Canvas(self.scrollable_frame_container, bg="#A32DC4", highlightthickness=0, height=500)  # Set the background color here
        self.canvas.grid(row=0, column=0, sticky="nsew", columnspan=3, rowspan=5)

        self.scrollbar = customtkinter.CTkScrollbar(self.scrollable_frame_container, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = customtkinter.CTkFrame(self.canvas, corner_radius=10, fg_color="transparent")  # Set the background color here
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.scrollable_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Load and process JSON data to create buttons
        self.load_json_and_create_buttons()
        
    def add_calculator_frame(self, seed):
        seed_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, seed +".png")), size=(45, 45))

        new_frame = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color="#DB90F0", height=25)
        new_frame.pack(pady=10, padx=10, fill="x")

        new_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        new_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        entry_seed = customtkinter.CTkEntry(new_frame, corner_radius=0, placeholder_text="Seed quantity")
        entry_seed.grid(row=1, column=2, padx=2, pady=0)

        seed_label = customtkinter.CTkLabel(new_frame, image=seed_image, text="")
        seed_label.grid(row=1, column=1)

        # Initialize labels with empty text
        cost = customtkinter.CTkLabel(new_frame, corner_radius=5, text="", fg_color="grey10", text_color="white")
        cost.grid(row=0, column=4, sticky="nsew", pady=6, padx=6)
        goldday = customtkinter.CTkLabel(new_frame, text="", fg_color="grey10", text_color="white")
        goldday.grid(row=1, column=4, sticky="nsew", pady=6, padx=6)
        netincome = customtkinter.CTkLabel(new_frame, text="", fg_color="grey10", text_color="white")
        netincome.grid(row=2, column=4, sticky="nsew", pady=6, padx=6)
        grossincome = customtkinter.CTkLabel(new_frame, corner_radius=5, text="", fg_color="grey10", text_color="white")
        grossincome.grid(row=3, column=4, sticky="nsew", pady=6, padx=6)

        equal = customtkinter.CTkLabel(new_frame, corner_radius=5, text="==", fg_color="transparent", text_color="white", font=customtkinter.CTkFont(size=45, weight="bold"))
        equal.grid(row=1, column=3, rowspan=2, sticky="nsew")

        destroy_frame = new_frame
        remove_button = customtkinter.CTkButton(new_frame, text="X", fg_color="red", text_color="white", width=20, corner_radius=10, height=0, command=lambda: self.kill_frame(destroy_frame))
        remove_button.grid(row=0, column=0, sticky="ns", rowspan=4, pady=0)

        # Update labels after calculation
        calculate_button = customtkinter.CTkButton(new_frame, text="Calcular", fg_color="black", text_color="white", border_width=2, 
                                                   command=lambda: self.calculator(seed, int(entry_seed.get()), cost, goldday, netincome, grossincome))
        calculate_button.grid(row=2, column=2)

    def load_json_and_create_buttons(self):
        with open("seeds.json", 'r') as file:
            data = json.load(file)

        row = 0
        column = 0
        for item in data["seeds"]:
            name = item["name"]
            image_file = os.path.join(self.image_path, f"{name}.png")

            if os.path.exists(image_file):
                image = customtkinter.CTkImage(Image.open(image_file), size=(45, 45))
                button = customtkinter.CTkButton(
                    self.crop_option_frame, text=name, image=image, compound="bottom", command=lambda n=name: self.add_calculator_frame(n)
                )
                button.grid(row=row, column=column, padx=10, pady=10)

                column += 1
                if column > 3:  # Adjusting for the new column count
                    column = 0
                    row += 1

    def kill_frame(self, frame):
        frame.destroy()

    def calculator(self, seed_name, seed_quantity, cost_label, goldday_label, netincome_label, grossincome_label):
        CC = calc()
        net_income = CC.net_income_per_month(seed_name, seed_quantity)
        gross_income = CC.gross_income_per_month(seed_name, seed_quantity)
        cost_of_plant = CC.needed_gold(seed_name, seed_quantity)
        gold_per_day = CC.gold_per_day(seed_name)

        # Update the labels with the calculated values
        cost_label.configure(text=f"Cost to plant: {cost_of_plant}g")
        goldday_label.configure(text=f"Gold per day: {gold_per_day}g")
        netincome_label.configure(text=f"Net income per month: {net_income}g")
        grossincome_label.configure(text=f"Gross income per month: {gross_income}g")

if __name__ == "__main__":
    app = App()
    app.mainloop()
