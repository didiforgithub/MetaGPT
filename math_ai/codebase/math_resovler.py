# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @Jiayi Zhang @ Fengwei Teng @ Yi Huang
# email      :
# Description: The Math Resolver is a core component of Math AI. Here, the Math Resolver will develop a plan based on the problem description and the strategy of the Gate Controller, selecting or recreating phase from the existing phase library, and invoking the LLM for solution finding.


from typing import Dict
from metagpt.roles.di.data_interpreter import DataInterpreter
from math_ai.codebase.engine.llm import OpenAILLM
from math_ai.codebase.prompt import zero_shot_planner, resolver_planner, inference_prompt, di_prompt, result_validate_prompt

# TODO add different phase in codebase.phase

async def main(requirement: str = ""):
    di = DataInterpreter()
    await di.run(requirement)

class MathResolver:
    def __init__(self):
        self.llm = OpenAILLM()
        self.role = "You're the most powerful math Olympiad in the world."
        self.llm.set_role(self.role)

    def run(problem:Dict, types:Dict):
        """
        problem: Dict
        types: {"strategy":"", "decompose":""} 
        """
        return {"current_trajectory": "current_trajectory"}

    async def single_run(self, problem: Dict, types: Dict) -> Dict:
        """
        Math Resolver resolve the problem based on the strategy from Gate Controller.
        First, math resolver need to develop a plan which contains basic phase (di for compute; logic validate for judge solution) to solve the problem.
        Then, math resolver need to ? <It's Complex Stage>
        Finally, math resolver need to return the solution without refine.
        """
        strategy_name = types["strategy"]
        strategy = ""

        # 1. 直接要求他解决数学问题，思考这个过程。 zero shot 让他先去对这个题目给出一个计划。
        # 2. 得到这个过程之后，让他结合我们的strategy 跟 Prompt，重新构建phase
        # 3. 每一个Phase的Prompt如何去写 

        origin_plan = self.llm.llm_response(prompt=zero_shot_planner.format(problem_desc=problem["desc"]),json_mode=True)
        resolver_plan = self.llm.llm_response(prompt=resolver_planner.format(problem_desc=problem["desc"], strategy=strategy, origin_plan=origin_plan), json_mode=True)
        
        current_trajectory = ""
        for phase in resolver_plan:
            if phase["plan"]["phase"] == "inference":
                # TODO 这里的Prompt 需要修改
                current_trajectory += self.inference(problem, current_trajectory, subgoal=phase["plan"]["desc"])
            elif phase["plan"]["phase"] == "di":
                current_trajectory += self.di_run(problem, current_trajectory, subgoal=phase["plan"]["desc"])
            elif phase["plan"]["phase"] == "logic_validate":
                # TODO 如果Validate 失败，是否需要重新进行plan
                current_trajectory += self.logic_validate(problem, current_trajectory, subgoal=phase["plan"]["desc"])
        
        # TODO 在这里result validate
        if self.result_validate(problem, current_trajectory):
            pass
        else:


        return {"current_trajectory": current_trajectory}
    
    async def multi_run(self):
        pass
    
    async def di_run(self, problem, current_trajectory, subgoal):
        # TODO 黄毅把获取的结果放到这里，我来写协程
        return "Hello world"
    
    def inference(self, problem, current_trajectory, subgoal):
        self.llm.llm_response(prompt=result_validate_prompt.format(problem=problem, trajectoty=current_trajectory),json_mode=True)
    
    def logic_validate(self, problem, current_trajectory, subgoal):
        self.llm.llm_response(prompt=result_validate_prompt.format(problem=problem, trajectoty=current_trajectory),json_mode=True)
        return "OK"
    
    def result_validate(self, problem, current_trajectory):
        validate_result = self.llm.llm_response(prompt=result_validate_prompt.format(problem=problem, trajectoty=current_trajectory),json_mode=True)
        return validate_result
    
    def inference_final(self, )