import React, {useRef, useEffect, useState} from "react";

function CameraPreview() {
    const videoRef = useRef<HTMLVideoElement>(null)
    const streamRef = useRef<MediaStream | null>(null)
    const [isCameraOn, setIsCameraOn] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)

    async function startCamera() {
        try {
            setError(null)

            const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 },
            },
            audio: false,
            })

            streamRef.current = stream
            if (videoRef.current) videoRef.current.srcObject = stream

            setIsCameraOn(true)
        }
        catch {
            setError("Failed to access camera. Check your browser permissions")
        }
    }

    function stopCamera() {
        streamRef.current?.getTracks().forEach((track) => track.stop())
        streamRef.current = null

        if (videoRef.current) videoRef.current.srcObject = null
        setIsCameraOn(false)
    }

    function toggleCamera(){
        isCameraOn ? stopCamera() : startCamera()
    }

    useEffect(() => {
        return () => stopCamera()
    }, [])

    return (
        <div className="camera">
            <video ref={videoRef} autoPlay muted playsInline/>
            <button onClick = {toggleCamera}>{isCameraOn ? "Stop Camera" : "Start Camera"}</button>
        </div>
    )
}

export default CameraPreview
