from fastapi import APIRouter
import gradio as gr

from app.models.service.ai import GenerativeAIService

web_router = APIRouter( prefix = "/widgets", tags = [ "Widgets" ] )

@web_router.get( "/" )
async def widgets_info():
    """Gradio UI interface, please visit `/widgets/chat`"""
    
    return { "message": "Gradio UI is available at /widget/..."}


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

bmi_calculator = gr.Interface( fn = calculate_bmi,
                               inputs = [ gr.Number( label = "weight", value = 50 ),
                                          gr.Number( label = "height", value = 1.6 ) ],
                               outputs = gr.Textbox( label = "BMI( Body Mass Index )", value = "0.0" ),
                               title = "BMI Calculator",
                               description = "Enter your weight and height to instantly get your BMI" )


def chat_function( question, history ):

    chat = GenerativeAIService.create_chat()

    input = ""
    for past_content in history:

        input += f"{past_content[ 'content' ]}\n"

    input += "記住以上對答的紀錄 繼續回答下面的問題\n"
    input += question
    # print( input )
    response = chat.send_message_stream( input )
    msg = ""
    for chunk in response:
        msg = msg + chunk.text
        yield msg

    # response = chat.send_message( input )
    # return response.text

chat_window = gr.ChatInterface( fn = chat_function, 
                                type = "messages", 
                                autofocus = True )