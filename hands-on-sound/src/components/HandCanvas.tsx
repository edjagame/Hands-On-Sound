import { useEffect, useRef } from 'react'
import { DrawingUtils, HandLandmarker } from '@mediapipe/tasks-vision'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'
interface HandCanvasProps {
  results: HandLandmarkerResult | null
  canvasWidth: number,
  canvasHeight: number,
}

function HandCanvas ({results, canvasHeight, canvasWidth}: HandCanvasProps){
    const canvasRef = useRef<HTMLCanvasElement>(null)
    
    useEffect(() => {
        const canvas = canvasRef.current
        if(!canvas) return
        const canvasCtx = canvas.getContext("2d")
        if(!canvasCtx) return
        const drawingUtils = new DrawingUtils(canvasCtx)

        canvasCtx.clearRect(0, 0, canvas.width, canvas.height)

        if(!results) return
        for(const landmarks of results.landmarks){
            drawingUtils.drawConnectors(
                landmarks,
                HandLandmarker.HAND_CONNECTIONS,
                {
                    color : "#00FF00",
                    lineWidth: 5
                }
            );
            drawingUtils.drawLandmarks( landmarks, {
                color: "#FF0000",
                lineWidth: 1
            });
        }   
    }, [results, canvasWidth, canvasHeight])

    return (
        <canvas 
            ref = {canvasRef}
            width = {canvasWidth}
            height = {canvasHeight}
        />
    )
}

export default HandCanvas