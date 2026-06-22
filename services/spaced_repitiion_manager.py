# IMPORTS
from datetime import datetime, timedelta


class SpacedRepetitionManager:
    
    def __init__(self):
        
        self.intervals = [1, 3, 7, 14, 22, 30]

    
    # Function to Determine the Next Review Date
    def next_review_date(self, stage_interv: int) -> str:

        # Validation
        if not isinstance(stage_interv, int):
            raise TypeError(f"Stage Intervals must be an integer.\n")
        
        if stage_interv < 0:
            raise ValueError(f"Stage intervals can only be positive.\n")
        
        if stage_interv >= len(self.intervals):
            stage_interv = len(self.intervals) - 1
        
        try:
            days = min(
                2** stage_interv, 
                365
            )
            review_date = datetime.now() + timedelta(days=days)

            return review_date.strftime("%Y-%m-%d")
        
        except OverflowError as e:
            raise OverflowError(f"Stage interval error is too large: {e}.\n")
        
        except Exception as e:
            raise Exception(f"Unexpected error: {e}.\n")
    

    # due_date() Function
    def is_due(self, review_date: str) -> bool:

        # Validation
        if not isinstance(review_date, str):
            raise TypeError(f"Review date must be a string.\n")
        
        if not review_date.strip():
            raise ValueError(f"Review date cannot be empty.\n")
        

        try:
            # Converts String of Datetime to Date
            review_datetime = datetime.strptime(review_date, "%Y-%m-%d")

            today_date = datetime.now()
            return today_date >= review_datetime
        
        except ValueError:
            raise ValueError(f"Review date format is 'YYYY-mm-dd'.\n")
        
        except Exception as e:
            raise Exception(f"Unexpected error: {e}.\n")




