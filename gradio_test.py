import gradio as gr

link: str = ('https://testbooru-cdn.donmai.us/original/f2/af/f2af745f037796cbd5088db4f0e2afd3.jpg', 'f2af745f037796cbd5088db4f0e2afd3.jpg')

def addNext(state: list[tuple[str,str]]):
    state.append(link)
    return [state, state]

with gr.Blocks() as demo:
    state = gr.State([])
    gallery = gr.Gallery(
        value=[],
    ).style(
        columns=6, rows=2, object_fit='contain', height=300, preview=False,
    )
    btn = gr.Button(label="Click me").click(
        fn=addNext,
        inputs=[state],
        outputs=[state,gallery]
    )
demo.launch()
