from .algorithm import Algorithm

class EDF(Algorithm):
    def calculate(self):
        print("\n performing EDF: \n")
        for i in range(self.max_timepoint):
            self.update_active_jobs(i)
            print(f"timepoint: {i}, active jobs: {self.active_jobs}")
    
    def summarize(self):
        print(f"\nEDF")
        super().summarize()
        pass

    def pick_next_job(self):
        return super().pick_next_job()
