from fastapi import APIRouter
import gradio as gr

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

from app.web.chat import chat_manager

healthcare_helper = chat_manager.genai_service
def chat_function( question, history ):

    try:
        qas = []
        for past_content in history:
            qas.append( f"{past_content[ 'role' ]}: {past_content[ 'content' ]}" )

        rag_prompt = healthcare_helper.rag_prompt( question )
        # print( rag_prompt )
        qas.append( rag_prompt )

        msg = ""
        for text in healthcare_helper.stream_answer( qas ):
            msg = msg + text
            yield msg

    except Exception as e:
        print( e )
        yield "Oops! Something went wrong. Please try again later."
    

chat_window = gr.ChatInterface( fn = chat_function,
                                examples = [ "提供哪些服務?", "該如何預防心臟病?", "該如何預防肝病?" ],
                                # editable = True,
                                type = "messages", 
                                autofocus = True )