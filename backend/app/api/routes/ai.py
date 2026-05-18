from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.routes.auth import get_current_user
from app.schemas.auth import ScriptToScenesRequest, ScriptToScenesResponse, UserOut
from app.services.ai_service import ai_service

router = APIRouter(tags=["ai"])


@router.post("/ai/script-to-scenes", response_model=ScriptToScenesResponse)
async def script_to_scenes(
    data: ScriptToScenesRequest,
    current_user: UserOut = Depends(get_current_user),
) -> dict[str, Any]:
    try:
        scenes = await ai_service.parse_script_to_scenes(
            script=data.script,
            tone=data.tone,
            max_scenes=data.max_scenes,
        )
        return {"scenes": scenes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/improve-script")
async def improve_script(
    script: str,
    feedback: str = "Make it more engaging",
    current_user: UserOut = Depends(get_current_user),
) -> dict[str, str]:
    try:
        improved = await ai_service.improve_script(script=script, feedback=feedback)
        return {"improved_script": improved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
