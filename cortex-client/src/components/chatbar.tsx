import "../styles/chatbar.css"
export default function Chatbar(){
    return(
        <div className="chatbargroup">
        <input type="text" className="textinput" placeholder="enter your prompt here" />
        <input type="button" className="" value="↑" />
        <input type="button" className="" value="🎙️" />
        </div>
    )
}