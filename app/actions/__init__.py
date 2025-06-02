


from app.actions.graphic_actions import RectangleDrawAction, ArrowDrawAction, CleanDrawedAction
from app.actions.pdf_actions import JPG2PDFConvertAction, MergePdfAction
from app.actions.start_actions import NotepadRunAction, CmdAdminRunAction, ZapretButton
from app.actions.text_actions import LayoutSwitchAction, TelegramAction, AITextConvertAction
from app.actions.time_actions import TimerQuick10Action, TimerQuick30Action, TimerQuick60Action, TimerDialogAction, TimersListAction

actions = [
    RectangleDrawAction, ArrowDrawAction, CleanDrawedAction, 
    JPG2PDFConvertAction, MergePdfAction,
    NotepadRunAction, CmdAdminRunAction, ZapretButton,
    LayoutSwitchAction, TelegramAction, AITextConvertAction,
    TimerQuick10Action, TimerQuick30Action, TimerQuick60Action, TimerDialogAction, TimersListAction,
]
