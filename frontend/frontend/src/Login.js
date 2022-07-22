import {useRef, useState, useEffect} from 'react'

const Login = () => {
    const userRef = useRef()
    const errRef = useRef()

    const[user, setUser] = useState('')
    const[pwd, setPwd] = useState('')
    const[errMsg, setErrMsg] = useState('')
    const[success, setSuccess] = useState(false)

    //.focus() will tell the browser which element is being acted on
    useEffect(() => {
        userRef.current.focus()
    }, [])

    //Empty out any error message if the user changes state
    useEffect(() => {
        setErrMsg('')
    }, [user, pwd])

    return (
        <section>
            {/* Throws error msg if user didnt fill user/password */}
            <p ref = {errRef} className = {errMsg ? "errmsg" : "offscreen"}
            aria-live= "assertive">{errMsg}</p>
            <h1>Sign In</h1>
            <form>
                {/* USERNAME */}
                <label htmlFor = "username">Username:</label>
                <input 
                type = "text" 
                id = "username"
                ref = {userRef}
                onChange = {(e) => setUser(e.target.value)}
                value = {user}
                required>
                </input> 

                {/* PASSWORD */}
                <label htmlFor = "password">Password:</label>
                <input 
                type = "password" 
                id = "password"
                onChange = {(e) => setPwd(e.target.value)}
                value = {pwd}
                required>
                </input> 
            </form>
            <p>
            </p>
        </section>
    )
}

export default Login