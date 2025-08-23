import gradio as gr

def calculate_bmi( weight_kg: float, height_m: float ):

    bmi = weight_kg / ( height_m ** 2 )
    category = ""

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal"
    elif 25 <= bmi < 30:
        category = "Overweight"
    elif bmi >= 30:
        category = "Obese"

    output_text = f"{bmi:.2f} ( {category} )"

    return output_text

container_css = """
.gradio-container {
    margin-left: auto;
    margin-right: auto;
    width: 600px;
    height: 700px;
}
"""

bmi_calculator = gr.Interface( fn = calculate_bmi,
                               inputs = [ gr.Number( label = "weight", value = 50 ),
                                          gr.Number( label = "height", value = 1.6 ) ],
                               outputs = gr.Textbox( label = "BMI( Body Mass Index )", value = "0.0" ),
                               title = "BMI Calculator",
                               description = "Enter your weight and height to instantly get your BMI",
                               css = container_css,
                               flagging_mode = "never"
)

