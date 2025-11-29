from enum import Enum
from dataclasses import dataclass
from typing import Dict, Union, Tuple, Optional, List
from llama_cpp import Llama

class ChatLlama:
    def __init__(self, model_path):
        from llama_cpp import Llama
        self.llm = Llama(model_path=model_path)

    def chat(self, prompt, max_tokens=200):
        out = self.llm(prompt, max_tokens=max_tokens)
        return out['choices'][0]['text'] 
class TaskType(Enum):
    # text2code
    web_code_retrieval = "Web Query to Code Retrieval"
    code_contest_retrieval = "Code Contest Retrieval"
    text2sql_retrieval = "Text to SQL Retrieval"
    error_message_retrieval = "Error Message to Code Retrieval"
    code_explanation_retrieval = "Code Explanation to Implementation Retrieval"
    api_usage_retrieval = "API Usage Description to Code Retrieval"
    bug_desc_retrieval = "Bug Description to Code Retrieval"
    pseudocode_retrieval = "Pseudocode to Code Retrieval"
    tutorial_query_retrieval = "Programming Tutorial Query to Code Example Retrieval"
    algorithm_desc_retrieval = "Algorithm Description to Code Retrieval"

    # code2text
    code_summary_retrieval = "Code Summary Retrieval"
    code_review_retrieval = "Code Review Retrieval"
    code_intent_retrieval = "Code Intent Retrieval"
    code_optimization_retrieval = "Code Optimization Retrieval"
    tutorial_retrieval = "Tutorial Retrieval"
    code_issue_discussion_retrieval = "Code Issue Discussion Retrieval"
    api_reference_retrieval = "API Reference Retrieval"
    code_walkthrough_retrieval = "Code Walkthrough Retrieval"
    code_error_explanation_retrieval = "Code Error Explanation Retrieval"
    code_to_requirement_retrieval = "Code to Requirement Retrieval"

    # code2code
    code_context_retrieval = "Code Context Retrieval"
    similar_code_retrieval = "Similar Code Retrieval"
    code_translation_retrieval = "Code Translation Retrieval"
    code_refinement_retrieval = "Code Refinement Retrieval"
    secure_code_retrieval = "Secure Code Retrieval"
    code_version_update_retrieval = "Code Version Update Retrieval"
    code_example_retrieval = "Code Example Retrieval"
    code_dependency_retrieval = "Code Dependency Retrieval"
    code_pattern_retrieval = "Code Pattern Retrieval"
    code_history_retrieval = "Code History Retrieval"
    code_integration_retrieval = "Code Integration Retrieval"
    optimized_code_retrieval = "Optimized Code Retrieval"
    code_simplification_retrieval = "Code Simplification Retrieval"
    code_modularization_retrieval = "Code Modularization Retrieval"
    code_augmentation_retrieval = "Code Augmentation Retrieval"
    error_handling_code_retrieval = "Error Handling Retrieval"
    code_documentation_retrieval = "Code Documentation Retrieval"
    library_adaptation_retrieval = "Library Adaptation Retrieval"

    # hybrid
    code_modification_retrieval = "Code Modification Retrieval"
    # single_turn_code_qa = "Single-turn Code QA"
    # multi_turn_code_qa = "Multi-turn Code QA"
    code_bug_fix_example_retrieval = "Code Bug Fix Example Retrieval"
    code_refactoring_pattern_retrieval = "Code Refactoring Pattern Retrieval"
    code_style_guideline_example_retrieval = "Code Style Guideline Example Retrieval"
    code_migration_retrieval = "Code Migration Retrieval"
    code_optimization_hybrid_retrieval = "Code Optimization Hybrid Retrieval"
    code_comparison_retrieval = "Code Comparison Retrieval"
    code_best_practices_retrieval = "Code Best Practices Retrieval"
    security_vulnerability_fix_retrieval = "Security Vulnerability Fix Retrieval"


def get_task_def_by_task_type(task_type: Union[str, TaskType]) -> Tuple[str, TaskType, str]:
    """
    Given a task type, return the main task type, task type, and task instruction.
    
    Args:
    - task_type: Union[str, TaskType]: the task type, either as a string or as a TaskType enum. Example: "web_code_retrieval" or TaskType.web_code_retrieval
    
    Returns:
    - main_task_type: str: the main task type. Example: "text2code"
    - task_type: TaskType: the task type. Example: TaskType.web_code_retrieval
    - task_instruction: str: the task instruction. Example: "Given a web search query, retrieve relevant code that can help answer the query."
    """
    
    task_type_to_instruct: Dict[TaskType, str] = {
        # text2code
        TaskType.web_code_retrieval: "Given a web search query, retrieve relevant code that can help answer the query.",
        TaskType.code_contest_retrieval: "Given a code contest problem description, retrieve relevant code that can help solve the problem.",
        TaskType.text2sql_retrieval: "Given a question in text, retrieve SQL queries that are appropriate responses to the question.",
        TaskType.error_message_retrieval: "Given an error message encountered during coding, retrieve relevant code that can help resolve the error.",
        TaskType.code_explanation_retrieval: "Given a textual explanation of code functionality, retrieve the corresponding code implementation.",
        TaskType.api_usage_retrieval: "Given a usage description of an API or library, retrieve code examples demonstrating the usage.",
        TaskType.bug_desc_retrieval: "Given a description of a software bug or unexpected behavior, retrieve relevant code that can help address the issue.",
        TaskType.pseudocode_retrieval: "Given a pseudocode description of an procedure, retrieve code implementations of the procedure.",
        TaskType.tutorial_query_retrieval: "Given a query related to a programming tutorial or learning material, retrieve code examples that are relevant to the query.",
        TaskType.algorithm_desc_retrieval: "Given a textual description of an algorithm, retrieve code implementations of the described algorithm.",
        
        # code2text
        TaskType.code_summary_retrieval: "Given a piece of code, retrieve the document string that summarizes the code.",
        TaskType.code_review_retrieval: "Given a piece of code, retrieve the review that explains its role.",
        TaskType.code_intent_retrieval: "Given a piece of code, retrieve the developer's intent or purpose described in a commit message or design document.",
        TaskType.code_optimization_retrieval: "Given a piece of code, retrieve optimization suggestions or performance analysis reports.",
        TaskType.tutorial_retrieval: "Given a piece of code, retrieve tutorials or how-to guides that demonstrate how to use or implement similar code.",
        TaskType.code_issue_discussion_retrieval: "Given a piece of code, retrieve discussions or issue reports related to the code, such as bug reports or feature requests.",
        TaskType.api_reference_retrieval: "Given a piece of code that uses specific APIs or libraries, retrieve the relevant API reference documentation for those APIs or libraries.",
        TaskType.code_walkthrough_retrieval: "Given a piece of code, retrieve a step-by-step walkthrough or detailed explanation of the code's logic and execution flow.",
        TaskType.code_error_explanation_retrieval: "Given a piece of code, retrieve the document that explains potential errors or exceptions that may arise from the code.",
        TaskType.code_to_requirement_retrieval: "Given a piece of code, retrieve the software requirement or user story it fulfills.",
        
        # code2code
        TaskType.code_context_retrieval: "Given a piece of code segment, retrieve the code segment that is the latter part of the code.",
        TaskType.similar_code_retrieval: "Given a piece of code, retrieve code that is semantically equivalent to the input code.",
        TaskType.code_translation_retrieval: "Given a piece of {src_language} code, retrieve {tgt_language} code that is semantically equivalent to the input code.",
        TaskType.code_refinement_retrieval: "Given a piece of code, retrieve a refined version of the code.",
        TaskType.secure_code_retrieval: "Given a piece of code, retrieve a version of the code with enhanced security measures or vulnerability fixes.",
        TaskType.code_version_update_retrieval: "Given a piece of code in an older language version, retrieve code updated to comply with the syntax or features of a newer language version.",
        TaskType.code_example_retrieval: "Given a code library or API, retrieve example code snippets that demonstrate how to use the library or API.",
        TaskType.code_dependency_retrieval: "Given a piece of code, retrieve all the code segments that the input code depends on, including libraries, functions, and variables.",
        TaskType.code_pattern_retrieval: "Given a piece of code, retrieve other code segments that follow the same design pattern or structure.",
        TaskType.code_history_retrieval: "Given a piece of code, retrieve previous versions or iterations of the code to understand its development history.",
        TaskType.code_integration_retrieval: "Given a piece of code, retrieve code that demonstrates how to integrate the input code with other systems or components.",
        TaskType.optimized_code_retrieval: "Given a piece of code, retrieve an optimized version of the code that improves performance, readability, or efficiency.",
        TaskType.code_simplification_retrieval: "Given a complex piece of code, retrieve a simplified version of the code that is easier to understand and maintain.",
        TaskType.code_modularization_retrieval: "Given a piece of code, retrieve a modularized version of the code that breaks it down into smaller, reusable components.",
        TaskType.code_augmentation_retrieval: "Given a piece of code, retrieve code that implements additional functionality while also preserving the original behavior.",
        TaskType.error_handling_code_retrieval: "Given a piece of code, retrieve code that incorporates error-checking or exception-handling mechanisms relevant to the input code.",
        TaskType.code_documentation_retrieval: "Given a piece of code, retrieve code with inline comments or documentation explaining its functionality.",
        TaskType.library_adaptation_retrieval: "Given a piece of code using one library or framework, retrieve code that achieves the same functionality using a different library or framework.",
        
        # hybrid
        TaskType.code_modification_retrieval: "Given a code snippet and a natural language description of desired modifications, retrieve relevant code that implements the requested modifications.",
        # TaskType.code_modification_retrieval: "Given a question that consists of a mix of text and code snippets, retrieve relevant code that answers the question.",
        # TaskType.single_turn_code_qa: "Given a question that consists of a mix of text and code snippets, retrieve relevant code that answer the question.",
        # TaskType.multi_turn_code_qa: "Given a multi-turn conversation history that consists of a mix of text and code snippets, retrieve relevant code that answer the question.",
        TaskType.code_bug_fix_example_retrieval: "Given a code snippet containing a bug and a natural language description of the bug or error, retrieve code snippets that demonstrate solutions or fixes for similar bugs or errors (the desired documents).",
        TaskType.code_refactoring_pattern_retrieval: "Given a code snippet that could be improved and a natural language description of desired refactoring goals or patterns, retrieve code snippets that exemplify similar refactoring techniques or patterns (the desired documents).",
        TaskType.code_style_guideline_example_retrieval: "Given a code snippet and a natural language query describing a desired coding style or best practice, retrieve code snippets that adhere to the specified style guidelines or best practices (the desired documents).",
        TaskType.code_migration_retrieval: "Given a code snippet and a natural language description of a specific migration requirement, retrieve code snippets that demonstrate how to migrate the code to meet the requirement.",
        TaskType.code_optimization_hybrid_retrieval: "Given a code snippet and a natural language request for specific optimization, retrieve relevant code that implements the requested optimization.",
        TaskType.code_comparison_retrieval: "Given two code snippets and a natural language query about their differences or similarities, retrieve relevant document that explains the differences or similarities between the two code snippets.",
        TaskType.code_best_practices_retrieval: "Given a code snippet and a natural language query about coding best practices, retrieve relevant document including guidelines, design patterns, or recommendations that can help improve the quality of the code.",
        TaskType.security_vulnerability_fix_retrieval: "Given a code snippet and a text description of a security concern, retrieve secure code alternatives that address the security vulnerability.",
    }
    
    task_type_to_main_type: Dict[TaskType, str] = {
        # text2code
        TaskType.web_code_retrieval: "text2code",
        TaskType.code_contest_retrieval: "text2code",
        TaskType.text2sql_retrieval: "text2code",
        TaskType.error_message_retrieval: "text2code",
        TaskType.code_explanation_retrieval: "text2code",
        TaskType.api_usage_retrieval: "text2code",
        TaskType.bug_desc_retrieval: "text2code",
        TaskType.pseudocode_retrieval: "text2code",
        TaskType.tutorial_query_retrieval: "text2code",
        TaskType.algorithm_desc_retrieval: "text2code",
        
        # code2text
        TaskType.code_summary_retrieval: "code2text",
        TaskType.code_review_retrieval: "code2text",
        TaskType.code_intent_retrieval: "code2text",
        TaskType.code_optimization_retrieval: "code2text",
        TaskType.tutorial_retrieval: "code2text",
        TaskType.code_issue_discussion_retrieval: "code2text",
        TaskType.api_reference_retrieval: "code2text",
        TaskType.code_walkthrough_retrieval: "code2text",
        TaskType.code_error_explanation_retrieval: "code2text",
        TaskType.code_to_requirement_retrieval: "code2text",
        
        # code2code
        TaskType.code_context_retrieval: "code2code",
        TaskType.similar_code_retrieval: "code2code",
        TaskType.code_translation_retrieval: "code2code",
        TaskType.code_refinement_retrieval: "code2code",
        TaskType.secure_code_retrieval: "code2code",
        TaskType.code_version_update_retrieval: "code2code",
        TaskType.code_example_retrieval: "code2code",
        TaskType.code_dependency_retrieval: "code2code",
        TaskType.code_pattern_retrieval: "code2code",
        TaskType.code_history_retrieval: "code2code",
        TaskType.code_integration_retrieval: "code2code",
        TaskType.optimized_code_retrieval: "code2code",
        TaskType.code_simplification_retrieval: "code2code",
        TaskType.code_modularization_retrieval: "code2code",
        TaskType.code_augmentation_retrieval: "code2code",
        TaskType.error_handling_code_retrieval: "code2code",
        TaskType.code_documentation_retrieval: "code2code",
        TaskType.library_adaptation_retrieval: "code2code",
        
        # hybrid
        TaskType.code_modification_retrieval: "hybrid",
        # TaskType.single_turn_code_qa: "hybrid",
        # TaskType.multi_turn_code_qa: "hybrid",
        TaskType.code_bug_fix_example_retrieval: "hybrid",
        TaskType.code_refactoring_pattern_retrieval: "hybrid",
        TaskType.code_style_guideline_example_retrieval: "hybrid",
        TaskType.code_migration_retrieval: "hybrid",
        TaskType.code_optimization_hybrid_retrieval: "hybrid",
        TaskType.code_comparison_retrieval: "hybrid",
        TaskType.code_best_practices_retrieval: "hybrid",
        TaskType.security_vulnerability_fix_retrieval: "hybrid",
    }

    if isinstance(task_type, str):
        task_type = TaskType[task_type]
    
    task_instruction = task_type_to_instruct[task_type]
    main_task_type = task_type_to_main_type[task_type]
    
    return main_task_type, task_type, task_instruction


class Language(Enum):
    en = 'English'  
    zh = 'Simplified Chinese'  
    
    ## Tasks: 1) web_code_retrieval, code_explanation_retrieval, text2sql_retrieval; 
    #         2) code_review_retrieval, code_walkthrough_retrieval, code_to_requirement_retrieval
    ## Code Languages: random sample 3 code languages
    ar = 'Arabic'  
    bn = 'Bengali' 
    es = 'Spanish' 
    fa = 'Persian'  
    fi = 'Finnish'  
    fr = 'French'  
    hi = 'Hindi'  
    id = 'Indonesian'  
    ja = 'Japanese'  
    ko = 'Korean'  
    ru = 'Russian'  
    sw = 'Swahili'  
    te = 'Telugu'  
    th = 'Thai'  
    de = 'German'
    yo = 'Yoruba'  
    it = 'Italian' 
    pt = 'Portuguese' 
    vi = 'Vietnamese'  
    zh_tw = 'Traditional Chinese'   

class CodeLanguage(Enum):
    # High (8): 3000 / language
    java = "Java"
    python = "Python"
    Python = "Python"
    javascript = "JavaScript"
    php = "PHP"
    ruby = "Ruby"
    go = "GO"
    csharp = "C#"
    cplusplus = "C++"
    # Medium (6): 1500 / language
    c = "C"
    rust = "Rust"
    typescript = "TypeScript"
    perl = "Perl"
    shell = "Shell"
    sql = "SQL"
    # Low (6): 750 / language
    batchfile = "Batchfile"
    fortran = "FORTRAN"
    haskell = "Haskell"
    lua = "Lua"
    powershell = "PowerShell"
    visual_basic = "Visual Basic"
    
    # NULL for tasks that do not require code language
    null = ""
    
  


# 16 * 2 = 32, 3000 per pair (32 * 3000 = 96000)
CODE_TRANSLATION_RETRIEVAL_PAIRS = [
    # c <-> cplusplus <-> csharp <-> java
    (CodeLanguage.c, CodeLanguage.cplusplus),
    (CodeLanguage.c, CodeLanguage.csharp),
    (CodeLanguage.c, CodeLanguage.java),
    (CodeLanguage.cplusplus, CodeLanguage.csharp),
    (CodeLanguage.cplusplus, CodeLanguage.java),
    (CodeLanguage.csharp, CodeLanguage.java),
    # python <-> ruby <-> perl
    (CodeLanguage.python, CodeLanguage.ruby),
    (CodeLanguage.python, CodeLanguage.perl),
    (CodeLanguage.ruby, CodeLanguage.perl),
    # javascript <-> typescript <-> php
    (CodeLanguage.javascript, CodeLanguage.typescript),
    (CodeLanguage.javascript, CodeLanguage.php),
    (CodeLanguage.typescript, CodeLanguage.php),
    # rust <-> go <-> cplusplus
    (CodeLanguage.rust, CodeLanguage.go),
    (CodeLanguage.rust, CodeLanguage.cplusplus),
    (CodeLanguage.go, CodeLanguage.cplusplus),
    # python <-> cplusplus
    (CodeLanguage.python, CodeLanguage.cplusplus),
]


@dataclass
class Task:
    task_type: TaskType
    language: Language
    code_language: CodeLanguage = CodeLanguage.null
    task_instruction: str = None
    tgt_code_language: CodeLanguage = CodeLanguage.null
    main_task_type: str = None


def get_task(
    task_type: str,
    language: str,
    code_language: str,
    tgt_code_language: Optional[str] = None
) -> Task:
    main_task_type, task_type, task_instruction = get_task_def_by_task_type(task_type)

    if tgt_code_language is None:
        tgt_code_language = "null"

    language = Language[language]
    code_language = CodeLanguage[code_language]
    tgt_code_language = CodeLanguage[tgt_code_language]

    task_instruction = task_instruction.replace("{src_language}", code_language.value).replace("{tgt_language}", tgt_code_language.value)

    task = Task(
        task_type=task_type,
        language=language,
        code_language=code_language,
        task_instruction=task_instruction,
        tgt_code_language=tgt_code_language,
        main_task_type=main_task_type
    )
    return task


SPECIAL_TASK_STEPS = {
    # TaskType.code_contest_retrieval: 2,
    TaskType.code_modification_retrieval: 2,
    TaskType.code_issue_discussion_retrieval: 2,
    TaskType.code_version_update_retrieval: 2,
    TaskType.code_bug_fix_example_retrieval: 2,
    TaskType.code_refactoring_pattern_retrieval: 2,
    TaskType.code_style_guideline_example_retrieval: 2,
    TaskType.bug_desc_retrieval: 2,
    TaskType.code_migration_retrieval: 2,
    TaskType.code_optimization_hybrid_retrieval: 2,
    TaskType.code_comparison_retrieval: 2,
    TaskType.code_best_practices_retrieval: 2,
    TaskType.security_vulnerability_fix_retrieval: 2,
}


def get_pos_as_input_by_task_type(task_type: TaskType) -> bool:
    """
    Get `pos_as_input` by task type.
    `pos_as_input=True` means that when generating a pair of query and pos, the pos is the input used for LLM generation. For example, text2code tasks: web_code_retrieval, code_contest_retrieval, text2sql_retrieval.
    `pos_as_input=False` means that when generating a pair of query and pos, the query is the input used for LLM generation. For example, code2text tasks: code_summary_retrieval, code_review_retrieval.
    """
    # TODO: Add more task types
    SPECIAL_TASKS = {
        # hybrid
        TaskType.code_bug_fix_example_retrieval: False,
        TaskType.code_refactoring_pattern_retrieval: False,
        TaskType.code_style_guideline_example_retrieval: False,
        TaskType.code_migration_retrieval: False,
        TaskType.code_optimization_hybrid_retrieval: False,
        TaskType.code_comparison_retrieval: False,
        TaskType.code_best_practices_retrieval: False,
        TaskType.security_vulnerability_fix_retrieval: False,
    }
    
    if task_type in SPECIAL_TASKS:
        return SPECIAL_TASKS[task_type]
    
    # normal rules
    main_task_type, _, _ = get_task_def_by_task_type(task_type)
    if main_task_type in ["text2code", "hybrid"]:
        return True
    elif main_task_type in ["code2text", "code2code"]:
        return False
    else:
        raise ValueError(f"Invalid task type: {task_type}")


def get_generation_prompt(
    task: Task,
    text: str,
    text_b: Optional[str] = None,
    examples: Optional[List[dict]] = None,
    idx: Optional[int] = None
) -> str:
    """
    Given a task, return the generation prompt for the task.
    
    Args:
    - task: Task: the task object
    - text: str: the input text
    - text_b: str: the second input text (optional), used for code_modification_retrieval task
    - examples: List[dict]: the examples for the task
    - idx: int: the index of gen_instruction in the instruction list (optional), used for tasks that need multiple steps to generate the output
    
    Returns:
    - gen_prompt: str: the generation prompt
    """
    
    task_to_gen_instruction: Dict[TaskType, str] = {
        # text2code (gen: code -> text)
        TaskType.web_code_retrieval: "Given a piece of {code_language} code, generate a web query in {language} that can be solved by the code.",
        TaskType.code_contest_retrieval: "Given a piece of {code_language} code, generate a code contest description in {language} that can be solved by the code.",
        TaskType.text2sql_retrieval: "Given a piece of {code_language} code, generate a text query in {language} for which the code is the appropriate response.",
        TaskType.error_message_retrieval: "Given a piece of {code_language} code, generate a possible error message in {language} that can be resolved by the code.",
        TaskType.code_explanation_retrieval: "Given a piece of {code_language} code, generate a textual explanation in {language} of the code functionality.",
        TaskType.api_usage_retrieval: "Given a piece of {code_language} code, generate a usage description of an API or library in {language} that can be demonstrated by the code as an example.",
        TaskType.bug_desc_retrieval: [
            "Given a piece of {code_language} code, modify some details of the code to introduce one or more bugs.",
            "Given a piece of {code_language} code with one or more bugs, generate a description of the bugs in {language}.",
        ],
        TaskType.pseudocode_retrieval: "Given a piece of {code_language} code, generate a pseudocode in {language} that describes the code functionality.",
        TaskType.tutorial_query_retrieval: "Given a piece of {code_language} code, generate a programming tutorial query in {language} that can be answered by the code as an example.",
        TaskType.algorithm_desc_retrieval: "Given a piece of {code_language} code, generate an algorithm description in {language} that can be implemented by the code.",
        
        # code2text (gen: code -> text)
        TaskType.code_summary_retrieval: "Given a piece of {code_language} code, generate a summary in {language} of the code.",
        TaskType.code_review_retrieval: "Given a piece of {code_language} code, generate a review in {language} that explains its role.",
        TaskType.code_intent_retrieval: "Given a piece of {code_language} code, generate a developer's intent or purpose described in a commit message or design document in {language}.",
        TaskType.code_optimization_retrieval: "Given a piece of {code_language} code, generate code optimization suggestions or performance analysis reports in {language}.",
        TaskType.tutorial_retrieval: "Given a piece of {code_language} code, generate tutorials or how-to guides that demonstrate how to use or implement similar code in {language}.",
        TaskType.code_issue_discussion_retrieval: [
            "Given a piece of {code_language} code, generate a version with some bugs.",
            "Given a piece of {code_language} code, generate a discussion of the code's issues or bugs in {language}, such as bug reports or feature requests.",
        ],
        TaskType.api_reference_retrieval: "Given a piece of {code_language} code, generate the relevant API reference documentation in {language} that can be used to understand the code.",
        TaskType.code_walkthrough_retrieval: "Given a piece of {code_language} code, generate a step-by-step walkthrough or detailed explanation of the code's logic and execution flow in {language}.",
        TaskType.code_error_explanation_retrieval: "Given a piece of {code_language} code, generate a detailed explanation of the errors or exceptions that may arise from the code in {language}.",
        TaskType.code_to_requirement_retrieval: "Given a piece of {code_language} code, generate a software requirement or user story it fulfills in {language}.",

        # code2code (gen: code-prefix -> code-suffix)
        TaskType.code_context_retrieval: "Given a piece of {code_language} code, generate a piece of code that is the latter part of the input code.",
        TaskType.similar_code_retrieval: "Given a piece of {code_language} code, generate a piece of {code_language} code that is semantically equivalent to the input code.",
        TaskType.code_translation_retrieval: "Given a piece of {code_language} code, generate a piece of {tgt_code_language} code that is semantically equivalent to the input code.",
        # src_language <-> code_language, tgt_language <-> tgt_code_language
        TaskType.code_refinement_retrieval: "Given a piece of {code_language} code, generate a refined version of the code.",
        TaskType.secure_code_retrieval: "Given a piece of {code_language} code, generate a a version of the code with enhanced security measures or vulnerability fixes.",
        TaskType.code_version_update_retrieval: [
            "Given a piece of {code_language} code, generate a lower-level version of the code.",
            "Given a piece of {code_language} code, update it with the syntax or features of a newer language version.",
        ],
        TaskType.code_example_retrieval: "Given a piece of {code_language} code, generate a piece of {code_language} code that is a good example of the code's usage.",
        TaskType.code_dependency_retrieval: "Given a piece of {code_language} code, generate the code segments that the input code depends on, including libraries, functions, and variables.",
        TaskType.code_pattern_retrieval: "Given a piece of {code_language} code, generate a piece of {code_language} code that follows the same design pattern or structure.",
        TaskType.code_history_retrieval: "Given a piece of {code_language} code, generate a piece of {code_language} code that is a historical version or iteration of the code.",
        TaskType.code_integration_retrieval: "Given a piece of {code_language} code, generate a piece of {code_language} code that integrates the input code with other systems or components.",
        TaskType.optimized_code_retrieval: "Given a piece of {code_language} code, generate an optimized version of the code that improves performance, readability, or efficiency.",
        TaskType.code_simplification_retrieval: "Given a piece of {code_language} code, generate a simplified version of the code that is easier to understand and maintain.",
        TaskType.code_modularization_retrieval: "Given a piece of {code_language} code, generate a modularized version of the code that breaks it down into smaller, reusable components.",
        TaskType.code_augmentation_retrieval: "Given a piece of {code_language} code, generate a piece of code that implements additional functionality while preserving the original behavior.",
        TaskType.error_handling_code_retrieval: "Given a piece of {code_language} code, generate a piece of code that incorporates error-checking or exception-handling mechanisms relevant to the input code.",
        TaskType.code_documentation_retrieval: "Given a piece of {code_language} code, generate a piece of code with inline comments or documentation explaining its functionality.",
        TaskType.library_adaptation_retrieval: "Given a piece of {code_language} code, generate a piece of code that achieves the same functionality using a different library or framework.",
        
        # hybrid (gen: code -> hybrid)
        TaskType.code_modification_retrieval: [
            "Given a piece of input code and a piece of output code, generate the differences in {language} between the input code and output code.",
            "Given the differences in {language} between a piece of input code and a piece of output code, generate a code modification instruction in {language} that uses only the information from the differences to transform the input code into the output code.",
        ],
        # TaskType.single_turn_code_qa: "Given a piece of code, generate a question that consists of a mix of {language} text and code snippets, and can be answered by the provided code.",
        # TaskType.multi_turn_code_qa: "Given a piece of code, generate a multi-turn conversation history that consists of a mix of {language} text and code snippets, and can be answered by the provided code.",
        TaskType.code_bug_fix_example_retrieval: [
            "Given a piece of {code_language} code, generate a buggy version of the code and a description in {language} of the bug or error.",
            "Given a piece of {code_language} code and a natural language description of the bug or error, generate a piece of {code_language} code that demonstrates a solution or fix for the bug or error.",
        ],
        TaskType.code_refactoring_pattern_retrieval: [
            "Given a piece of {code_language} code, generate a description of the desired refactoring goals or patterns in {language}.",
            "Given a piece of {code_language} code and a natural language description of the desired refactoring goals or patterns, generate a piece of {code_language} code that exemplifies similar refactoring techniques or patterns.",
        ],
        TaskType.code_style_guideline_example_retrieval: [
            "Given a piece of {code_language} code, generate a query describing a desired coding style or best practice to improve it in {language}.",
            "Given a piece of {code_language} code and a natural language query describing the desired style guidelines or best practices, generate a piece of {code_language} code that adheres to the specified style guidelines or best practices.",
        ],
        TaskType.code_migration_retrieval: [
            "Given a piece of {code_language} code, generate a specific migration requirement in {language} based on the code.",
            "Given a piece of {code_language} code and a natural language description of a specific migration requirement, generate a piece of {code_language} code that meets the migration requirement.",
        ],
        TaskType.code_optimization_hybrid_retrieval: [
            "Given a piece of {code_language} code, generate a question in {language} that requests a specific optimization for the code.",
            "Given a piece of {code_language} code and a natural language request in {language} for specific optimization, generate a piece of output code that implements the requested optimization.",
        ],
        TaskType.code_comparison_retrieval: [
            "Given a piece of input code and a piece of output code, generate a question in {language} about their differences or similarities.",
            "Given a piece of input code and a piece of output code, and a natural language question in {language} about their differences or similarities, generate a response that answer the question.",
        ],
        TaskType.code_best_practices_retrieval: [
            "Given a piece of {code_language} code, generate a question in {language} about coding best practices related to the code.",
            "Given a piece of {code_language} code and a natural language question in {language} about coding best practices related to the code, generate a response including guidelines, design patterns, or recommendations that can help improve the quality of the code.",
        ],
        TaskType.security_vulnerability_fix_retrieval: [
            "Given a piece of {code_language} code, generate a text description in {language} of a possible security concern in the code.",
            "Given a piece of {code_language} code and a text description in {language} of a security concern, generate secure code alternatives that address the vulnerability.",
        ],
    }
    
    task_to_gen_output: Dict[TaskType, str] = {
        # text2code (gen: code -> text)
        TaskType.web_code_retrieval: "the generated web query in {language}",
        TaskType.code_contest_retrieval: "the generated code contest description in {language}",
        TaskType.text2sql_retrieval: "the generated text query in {language}",
        TaskType.error_message_retrieval: "the generated error message in {language}",
        TaskType.code_explanation_retrieval: "the generated explanation in {language}",
        TaskType.api_usage_retrieval: "the generated API or library usage description in {language}",
        TaskType.bug_desc_retrieval: [
            "the modified code with one or more bugs",
            "the generated bug description in {language}",
        ],
        TaskType.pseudocode_retrieval: "the generated pseudocode in {language}",
        TaskType.tutorial_query_retrieval: "the generated programming tutorial query in {language}",
        TaskType.algorithm_desc_retrieval: "the generated algorithm description in {language}",
        
        # code2text (gen: code -> text)
        TaskType.code_summary_retrieval: "the generated summary in {language}",
        TaskType.code_review_retrieval: "the generated review in {language}",
        TaskType.code_intent_retrieval: "the generated intent in {language}",
        TaskType.code_optimization_retrieval: "the generated optimization suggestions or performance analysis reports in {language}",
        TaskType.tutorial_retrieval: "the generated tutorial in {language}",
        TaskType.code_issue_discussion_retrieval: [
            "the generated buggy code",
            "the generated error explanation in {language}",
        ],
        TaskType.api_reference_retrieval: "the generated API reference documentation in {language}",
        TaskType.code_walkthrough_retrieval: "the generated walkthrough in {language}",
        TaskType.code_error_explanation_retrieval: "the generated error explanation in {language}",
        TaskType.code_to_requirement_retrieval: "the generated requirement in {language}",

        # code2code (gen: code-prefix -> code-suffix)
        TaskType.code_context_retrieval: "the generated piece of {code_language} code",
        TaskType.similar_code_retrieval: "the generated piece of {code_language} code",
        TaskType.code_translation_retrieval: "the generated piece of {tgt_code_language} code",
        TaskType.code_refinement_retrieval: "the generated piece of {code_language} code",
        TaskType.secure_code_retrieval: "the generated piece of {code_language} code",
        TaskType.code_version_update_retrieval: [
            "the generated piece of {code_language} code",
            "the generated piece of {code_language} code",
        ],
        TaskType.code_example_retrieval: "the generated piece of {code_language} code",
        TaskType.code_dependency_retrieval: "the generated piece of {code_language} code",
        TaskType.code_pattern_retrieval: "the generated piece of {code_language} code",
        TaskType.code_history_retrieval: "the generated piece of {code_language} code",
        TaskType.code_integration_retrieval: "the generated piece of {code_language} code",
        TaskType.optimized_code_retrieval: "the generated piece of {code_language} code",
        TaskType.code_simplification_retrieval: "the generated piece of {code_language} code",
        TaskType.code_modularization_retrieval: "the generated piece of {code_language} code",
        TaskType.code_modification_retrieval: "the generated piece of {code_language} code",
        TaskType.code_augmentation_retrieval: "the generated piece of {code_language} code",
        TaskType.error_handling_code_retrieval: "the generated piece of {code_language} code",
        TaskType.code_documentation_retrieval: "the generated piece of {code_language} code",
        TaskType.library_adaptation_retrieval: "the generated piece of {code_language} code",
        
        # hybrid (gen: code -> hybrid)
        TaskType.code_modification_retrieval: [
            "the generated differences in {language} between the input code and output code",
            "the generated modification instruction in {language}",
        ],
        # TaskType.single_turn_code_qa: "the generated question that consists of a mix of {language} text and code snippets",
        # TaskType.multi_turn_code_qa: "the generated multi-turn conversation history that consists of a mix of {language} text and code snippets",
        TaskType.code_bug_fix_example_retrieval: [
            "the generated buggy version of the code and a description in {language} of the bug or error",
            "the generated piece of {code_language} code"
        ],
        TaskType.code_refactoring_pattern_retrieval: [
            "the generated description of the desired refactoring goals or patterns in {language}",
            "the generated piece of {code_language} code"
        ],
        TaskType.code_style_guideline_example_retrieval: [
            "the generated query describing a desired coding style or best practice to improve it in {language}",
            "the generated piece of {code_language} code"
        ],
        TaskType.code_migration_retrieval: [
            "the generated specific migration requirement in {language} based on the code",
            "the generated piece of {code_language} code"
        ],
        TaskType.code_optimization_hybrid_retrieval: [
            "the generated question in {language} that requests a specific optimization for the code",
            "the generated piece of {code_language} code",
        ],
        TaskType.code_comparison_retrieval: [
            "the generated question in {language} about their differences or similarities",
            "the generated response in {language}",
        ],
        TaskType.code_best_practices_retrieval: [
            "the generated question in {language} about coding best practices related to the code",
            "the generated response in {language}",
        ],
        TaskType.security_vulnerability_fix_retrieval: [
            "the generated text description in {language} of a possible security concern in the code",
            "the generated piece of {code_language} code",
        ],
    }
    
    gen_instruction = task_to_gen_instruction[task.task_type]
    gen_output = task_to_gen_output[task.task_type]
    
    if idx is not None:
        assert isinstance(gen_instruction, list)
        gen_instruction = gen_instruction[idx]
        assert isinstance(gen_output, list)
        gen_output = gen_output[idx]
    
    assert isinstance(gen_instruction, str)
    assert isinstance(gen_output, str)
    
    gen_instruction = gen_instruction.replace("{language}", task.language.value).replace("{code_language}", task.code_language.value).replace("{tgt_code_language}", task.tgt_code_language.value)
    gen_output = gen_output.replace("{language}", task.language.value).replace("{code_language}", task.code_language.value).replace("{tgt_code_language}", task.tgt_code_language.value)
    
    if task.task_type == TaskType.code_modification_retrieval:
        if idx == 0:
            assert text_b is not None
            gen_prompt = f"""\
{gen_instruction}

Input code:
```{task.code_language.name}
{text}
```

Output code:
```{task.code_language.name}
{text_b}
```

Note:
- Your output must always be a string, only containing {gen_output}.
- Your output should be independent of the given code, which means that it should not contain the pronouns such as "it", "this", "that", "the given", "the provided", etc.

Remember do not explain your output or output anything else. Your output:"""
            return gen_prompt
        elif idx == 1:
            prefix = "Differences:"
        else:
            raise ValueError("Invalid idx for code_modification_retrieval task")
    elif task.task_type == TaskType.code_comparison_retrieval:
        if idx == 0:
            assert text_b is not None
            gen_prompt = f"""\
{gen_instruction}

Input code:
```{task.code_language.name}
{text}
```

Output code:
```{task.code_language.name}
{text_b}
```

Note:
- Your output must always be a string, only containing {gen_output}.
- Your output should be independent of the given code, which means that it should not contain the pronouns such as "it", "this", "that", "the given", "the provided", etc.

Remember do not explain your output or output anything else. Your output:"""
            return gen_prompt
        elif idx == 1:
            prefix = "Hybrid:"
        else:
            raise ValueError("Invalid idx for code_comparison_retrieval task")
    elif task.task_type in [
        TaskType.code_bug_fix_example_retrieval,
        TaskType.code_refactoring_pattern_retrieval,
        TaskType.code_style_guideline_example_retrieval,
        TaskType.code_migration_retrieval,
        TaskType.code_optimization_hybrid_retrieval,
        TaskType.code_best_practices_retrieval,
        TaskType.security_vulnerability_fix_retrieval,
    ]:
        if idx == 0:
            prefix = "Code:"
        elif idx == 1:
            prefix = "Hybrid:"
        else:
            raise ValueError("Invalid idx for hybrid task")
    else:
        prefix = "Code:"

    gen_prompt = f"""\
{gen_instruction}

{prefix}
```{task.code_language.name}
{text}
```

Note:
- Your output must always be a string, only containing {gen_output}.
- Your output should be independent of the given code, which means that it should not contain the pronouns such as "it", "this", "that", "the given", "the provided", etc.

"""

    if idx != 0 and examples is not None:
        examples_str_list = [f"""\
- Example {i + 1}:
    {prefix}
    ```{task.code_language.name}
    {example['input']}
    ```
    Expected Output ({gen_output}):
    ```
    {example['output']}
    ```

""" for i, example in enumerate(examples)]
        
        gen_prompt += f"""\
Here are a few examples for your reference:
{''.join(examples_str_list)}
"""

    gen_prompt += "Remember do not explain your output or output anything else. Your output:"

    return gen_prompt


def get_quality_control_prompt(
    task: Task,
    query: str,
    pos: str,
) -> str:
    """
    Given a task, return the quality control prompt for the task.
    
    Args:
    - task: Task: the task object
    
    Returns:
    - qc_prompt: str: the quality control prompt
    """
    
    # return tuples of (mission, query_type, doc_type, qc_options)
    task_to_qc_mission: Dict[TaskType, str] = {
        # text2code
        TaskType.web_code_retrieval: (
            "judge whether the code can help answer the web search query",
            "the web search query",
            "the code",
            [
                "Yes, the code can help answer the web search query.",
                "No, the code cannot help answer the web search query.",
            ]
        ),
        TaskType.code_contest_retrieval: (
            "judge whether the code can help solve the code contest problem",
            "the code contest problem",
            "the code",
            [
                "Yes, the code can help solve the code contest problem.",
                "No, the code cannot help solve the code contest problem.",
            ]
        ),
        TaskType.text2sql_retrieval: (
            "judge whether the code is an appropriate response to the text query",
            "the text query",
            "the code",
            [
                "Yes, the code is an appropriate response to the text query.",
                "No, the code is not an appropriate response to the text query.",
            ]
        ),
        TaskType.error_message_retrieval: (
            "judge whether the code can help resolve the error message",
            "the error message",
            "the code",
            [
                "Yes, the code can help resolve the error message.",
                "No, the code cannot help resolve the error message.",
            ]
        ),
        TaskType.code_explanation_retrieval: (
            "judge whether the code implements the functionality described in the explanation",
            "the explanation",
            "the code",
            [
                "Yes, the code implements the functionality described in the explanation.",
                "No, the code does not implement the functionality described in the explanation.",
            ]
        ),
        TaskType.api_usage_retrieval: (
            "judge whether the code demonstrates the usage description of the API or library",
            "the API or library usage description",
            "the code",
            [
                "Yes, and the code demonstrates the usage description of the API or library.",
                "No, the code does not demonstrate the usage description of the API or library.",
            ]
        ),
        TaskType.bug_desc_retrieval: (
            "judge whether the code can help address the described bug",
            "the bug description",
            "the code",
            [
                "Yes, the code can help address the described bug.",
                "No, the code cannot help address the described bug.",
            ]
        ),
        TaskType.pseudocode_retrieval: (
            "judge whether the code implements the procedure described in the pseudocode",
            "the pseudocode",
            "the code",
            [
                "Yes, the code implements the procedure described in the pseudocode.",
                "No, the code does not implement the procedure described in the pseudocode.",
            ]
        ),
        TaskType.tutorial_query_retrieval: (
            "judge whether the code can answer the programming tutorial query",
            "the programming tutorial query",
            "the code",
            [
                "Yes, the code can answer the programming tutorial query.",
                "No, the code cannot answer the programming tutorial query.",
            ]
        ),
        TaskType.algorithm_desc_retrieval: (
            "judge whether the code implements the algorithm described in the text",
            "the algorithm description",
            "the code",
            [
                "Yes, the code implements the algorithm described in the text.",
                "No, the code does not implement the algorithm described in the text.",
            ]
        ),
        
        # code2text
        TaskType.code_summary_retrieval: (
            "judge whether the text summarizes the code",
            "the code",
            "the text",
            [
                "Yes, the text summarizes the code.",
                "No, the text does not summarize the code.",
            ]
        ),
        TaskType.code_review_retrieval: (
            "judge whether the review explains the role of the code",
            "the code",
            "the review",
            [
                "Yes, the review explains the role of the code.",
                "No, the review does not explain the role of the code.",
            ]
        ),
        TaskType.code_intent_retrieval: (
            "judge whether the text describes the intent of the code",
            "the code",
            "the text",
            [
                "Yes, the text describes the intent of the code.",
                "No, the text does not describe the intent of the code.",
            ]
        ),
        TaskType.code_optimization_retrieval: (
            "judge whether the text provides optimization suggestions or performance analysis reports for the code",
            "the code",
            "the text",
            [
                "Yes, the text provides optimization suggestions or performance analysis reports for the code.",
                "No, the text provides neither optimization suggestions nor performance analysis reports for the code.",
            ]
        ),
        TaskType.tutorial_retrieval: (
            "judge whether the text is a tutorial or how-to guide that demonstrates how to use or implement similar code",
            "the code",
            "the text",
            [
                "Yes, the text is a tutorial or how-to guide that demonstrates how to use or implement similar code.",
                "No, the text neither provides instructional guidance for using similar code nor demonstrates how to implement similar code.",
            ]
        ),
        TaskType.code_error_explanation_retrieval: (
            "judge whether the text describes potential errors or exceptions that may arise from the code",
            "the code",
            "the text",
            [
                "Yes, the text describes potential errors or exceptions that may arise from the code.",
                "No, the text neither describes potential errors nor discuss exceptions that may arise from the code.",
            ]
        ),
        TaskType.code_issue_discussion_retrieval: (
            "judge whether the text is a discussion or issue report related to the code",
            "the code",
            "the text",
            [
                "Yes, the text is a discussion or issue report related to the code.",
                "No, the text is neither a discussion about the code nor an issue report related to the code.",
            ]
        ),
        TaskType.api_reference_retrieval: (
            "judge whether the text is an API reference documentation for the APIs or libraries used in the code",
            "the code",
            "the text",
            [
                "Yes, the text is an API reference documentation for the APIs or libraries used in the code.",
                "No, the text is not an API reference documentation for the APIs or libraries used in the code.",
            ]
        ),
        TaskType.code_walkthrough_retrieval: (
            "judge whether the text is a step-by-step walkthrough or detailed explanation of the code's logic and execution flow",
            "the code",
            "the text",
            [
                "Yes, the text is a step-by-step walkthrough or detailed explanation of the code's logic and execution flow.",
                "No, the text is neither a step-by-step walkthrough nor a detailed explanation of the code's logic and execution flow.",
            ]
        ),
        TaskType.code_to_requirement_retrieval: (
            "judge whether the text is a software requirement or user story that the code fulfills",
            "the code",
            "the text",
            [
                "Yes, the text is a software requirement or user story that the code fulfills.",
                "No, the text is neither a software requirement nor a user story that the code fulfills.",
            ]
        ),
        
        # code2code
        TaskType.code_context_retrieval: (
            "judge whether the output code is the latter part of the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is the latter part of the input code.",
                "No, the output code is not the latter part of the input code.",
            ]
        ),
        TaskType.similar_code_retrieval: (
            "judge whether the output code is semantically equivalent to the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is semantically equivalent to the input code.",
                "No, the output code is not semantically equivalent to the input code.",
            ]
        ),
        TaskType.code_translation_retrieval: (
            "judge whether the output code is semantically equivalent to the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is semantically equivalent to the input code.",
                "No, the output code is not semantically equivalent to the input code.",
            ]
        ),
        TaskType.code_refinement_retrieval: (
            "judge whether the output code is a refined version of the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is a refined version of the input code.",
                "No, the output code is not a refined version of the input code.",
            ]
        ),
        TaskType.secure_code_retrieval: (
            "judge whether the output code is the version with enhanced security measures or vulnerability fixes compared to the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is the version with enhanced security measures or vulnerability fixes compared to the input code.",
                "No, the output code neither introduces security enhancements nor fixes vulnerabilities compared to the input code.",
            ]
        ),
        TaskType.code_version_update_retrieval: (
            "judge whether the output code is the version updated to comply with the syntax or features of a newer language version compared to the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is the version updated to comply with the syntax or features of a newer code language version compared to the input code.",
                "No, the output code neither adopts syntax updates nor introduces newer code language features compared to the input code.",
            ]
        ),
        TaskType.code_example_retrieval: (
            "judge whether the output code is the example code snippets that demonstrate how to use the library or API in the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is the example code snippets that demonstrate how to use the library or API in the input code.",
                "No, the output code is not the example code snippets that demonstrate how to use the library or API in the input code.",
            ]
        ),
        TaskType.code_dependency_retrieval: (
            "judge whether the output code is the code segments that the input code depends on, including libraries, functions, and variables.",
            "the input code",
            "the output code",
            [
                "Yes, the output code is the code segments that the input code depends on, including libraries, functions, and variables.",
                "No, the output code is not the code segments that the input code depends on, including libraries, functions, and variables.",
            ]
        ),
        TaskType.code_pattern_retrieval: (
            "judge whether the output code follows the same design pattern or structure as the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code follows the same design pattern or structure as the input code.",
                "No, the output code neither follows the same design pattern nor retains the same structure as the input code.",
            ]
        ),
        TaskType.code_history_retrieval: (
            "judge whether the output code is the historical version or iteration of the input code, and can help understand its development history.",
            "the input code",
            "the output code",
            [
                "Yes, the output code is the historical version or iteration of the input code, and can help understand its development history.",
                "No, the output code is not the historical version or iteration of the input code, and cannot help understand its development history.",
            ]
        ),
        TaskType.code_integration_retrieval: (
            "judge whether the output code demonstrates how to integrate the input code with other systems or components.",
            "the input code",
            "the output code",
            [
                "Yes, the output code demonstrates how to integrate the input code with other systems or components.",
                "No, the output code does not demonstrate how to integrate the input code with other systems or components.",
            ]
        ),
        TaskType.optimized_code_retrieval: (
            "judge whether the output code is an optimized version of the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is an optimized version of the input code.",
                "No, the output code is not an optimized version of the input code.",
            ]
        ),
        TaskType.code_simplification_retrieval: (
            "judge whether the output code is a simplified version of the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is a simplified version of the input code.",
                "No, the output code is not a simplified version of the input code.",
            ]
        ),
        TaskType.code_modularization_retrieval: (
            "judge whether the output code is a modularized version of the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code is a modularized version of the input code.",
                "No, the output code is not a modularized version of the input code.",
            ]
        ),
        TaskType.code_augmentation_retrieval: (
            "judge whether the output code implements additional functionality while preserving the original behavior of the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code implements additional functionality while preserving the original behavior of the input code.",
                "No, the output code does not implement additional functionality while preserving the original behavior of the input code.",
            ]
        ),
        TaskType.error_handling_code_retrieval: (
            "judge whether the output code incorporates error-checking or exception-handling mechanisms relevant to the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code incorporates error-checking or exception-handling mechanisms relevant to the input code.",
                "No, the output code does not incorporate error-checking or exception-handling mechanisms relevant to the input code.",
            ]
        ),
        TaskType.code_documentation_retrieval: (
            "judge whether the output code contains inline comments or documentation explaining the functionality of the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code contains inline comments or documentation explaining the functionality of the input code.",
                "No, the output code does not contain inline comments or documentation explaining the functionality of the input code.",
            ]
        ),
        TaskType.library_adaptation_retrieval: (
            "judge whether the output code achieves the same functionality using a different library or framework as the input code",
            "the input code",
            "the output code",
            [
                "Yes, the output code achieves the same functionality using a different library or framework as the input code.",
                "No, the output code does not achieve the same functionality using a different library or framework as the input code.",
            ]
        ),
        
        # hybrid
        TaskType.code_modification_retrieval: (
            "judge whether the output code implements the requested modification described in the query",
            "the query",
            "the output code",
            [
                "Yes, the output code implements the requested modification described in the query.",
                "No, the output code does not implement the requested modification described in the query.",
            ]
        ),
        # TaskType.single_turn_code_qa: "judge whether the output code can answer the question",
        # TaskType.multi_turn_code_qa: "judge whether the output code can answer the question",
        TaskType.code_bug_fix_example_retrieval: (
            "judge whether the output code fixes the bug or error described in the query.",
            "the query",
            "the output code",
            [
                "Yes, the output code fixes the bug or error described in the query.",
                "No, the output code does not fix the bug or error described in the query.",
            ]
        ),
        TaskType.code_refactoring_pattern_retrieval: (
            "judge whether the output code exemplifies similar refactoring techniques or patterns described in the query",
            "the query",
            "the output code",
            [
                "Yes, the output code exemplifies similar refactoring techniques or patterns described in the query.",
                "No, the output code does not exemplify similar refactoring techniques or patterns described in the query.",
            ]
        ),
        TaskType.code_style_guideline_example_retrieval: (
            "judge whether the output code adheres to the specified style guidelines or best practices described in the query",
            "the query",
            "the output code",
            [
                "Yes, the output code adheres to the specified style guidelines or best practices described in the query.",
                "No, the output code does not adhere to the specified style guidelines or best practices described in the query.",
            ]
        ),
        TaskType.code_migration_retrieval: (
            "judge whether the output code meets the migration requirement described in the query",
            "the query",
            "the output code",
            [
                "Yes, the output code meets the migration requirement described in the query.",
                "No, the output code does not meet the migration requirement described in the query.",
            ]
        ),
        TaskType.code_optimization_hybrid_retrieval: (
            "judge whether the output code implements the requested optimization described in the query",
            "the query",
            "the output code",
            [
                "Yes, the output code implements the requested optimization described in the query.",
                "No, the output code does not implement the requested optimization described in the query.",
            ]
        ),
        TaskType.code_comparison_retrieval: (
            "judge whether the response can answer the question described in the query",
            "the query",
            "the response",
            [
                "Yes, the response can answer the question described in the query.",
                "No, the response cannot answer the question described in the query.",
            ]
        ),
        TaskType.code_best_practices_retrieval: (
            "judge whether the response can answer the question described in the query",
            "the query",
            "the response",
            [
                "Yes, the response can answer the question described in the query.",
                "No, the response cannot answer the question described in the query.",
            ]
        ),
        TaskType.security_vulnerability_fix_retrieval: (
            "judge whether the output code addresses the security vulnerability described in the query",
            "the query",
            "the output code",
            [
                "Yes, the output code addresses the security vulnerability described in the query.",
                "No, the output code does not address the security vulnerability described in the query.",
            ]
        ),
    }
    
    if task.main_task_type == "text2code":
        type_check_option = "the query contains code snippets or the document contains non-code content (plain text)."
    elif task.main_task_type == "code2text":
        type_check_option = "the query contains non-code content (plain text) or the document contains code snippets."
    elif task.main_task_type == "code2code":
        type_check_option = "either the query or the document contains non-code content (plain text)."
    else:
        type_check_option = "neither the query nor the document contains the mixed content of code and text content."
    
    qc_mission, query_type, doc_type, qc_options = task_to_qc_mission[task.task_type]
    
    pos_option = qc_options[0]
    neg_option = qc_options[1]
    
    qc_prompt = f"""\
Given a code retrieval task (Task), a query (Query), and a document (Document), your mission is to {qc_mission}.

Task ({task.main_task_type}): {task.task_instruction}

Query ({query_type}):
```
{query}
```

Document ({doc_type}):
```
{pos}
```

Your output must be one of the following options:
- 0: The query or document does not match the main task type ({task.main_task_type}), which means that {type_check_option}
- 1: The query and document match the main task type ({task.main_task_type}). The judgment is: {pos_option}
- 2: The query and document match the main task type ({task.main_task_type}). The judgment is: {neg_option}

Do not explain your answer in the output. Your output must be a single number (0 or 1 or 2).

Your output:"""
    
    return qc_prompt


class DocLength(Enum):
    len_0_500 = "_len-0-500.jsonl"
    len_500_1000 = "_len-500-1000.jsonl"
    len_1000_2000 = "_len-1000-2000.jsonl"
    len_2000_4000 = "_len-2000-4000.jsonl"
    len_4000_8000 = "_len-4000-8000.jsonl"
    len_8000_16000 = "_len-8000-16000.jsonl"
    len_16000_32000 = "_len-16000-32000.jsonl"


# only used for paper cmp: gen hard negative v.s. mine hard negative
def get_gen_hard_neg_prompt(task: Task, query: str, pos: str) -> str:
    """
    Given a task, return the generation hard negative prompt for the task.
    
    Args:
    - task: Task: the task object

    Returns:
    - gen_hard_neg_prompt: str: the generation hard negative prompt
    """
    gen_hard_neg_prompt = f"""\
Given a code retrieval task (Task), a query (Query), and a positive document (Positive Document), your mission is to generate a hard negative document that only appears relevant to the query under the code retrieval task.

Task ({task.main_task_type}): {task.task_instruction}

Query:
```
{query}
```

Positive Document:
```
{pos}
```

Note:
- Your output must always be a string, only containing the hard negative document.
- The hard negative document should be similar to the positive document in terms of content. If the positive document is a code snippet, the hard negative document should also be a code snippet. If the positive document is a text description, the hard negative document should also be a text description.

Remember do not explain your output or output anything else. Your output:"""

    return gen_hard_neg_prompt


NUM_HARD_NEGATIVES = 7


import re

def clean_content(content: str):
    if content is None:
        raise ValueError("content is None.")
    
    content = content.split('</think>')[-1].strip('\n').strip()
    
    if content.startswith('\"') and content.endswith('\"'):
        content = content[1:-1]
    
    if content.startswith("```\n") and content.endswith("\n```"):
        content = content[4:-4]
    
    return content


def clean_code(code: str, lang: str, length_threshold: int = 30) -> str:
    cleaned_code = code.strip('\ufeff').strip()
    if not cleaned_code:
        return ''

    def clean_empty_lines(text: str) -> str:
        return re.sub(r'\n\s*\n', '\n', text).strip()

    function_patterns = {
        "java": r"(?m)^(?!\s*(import|package)\b).*\b(public\s+class|class\s+\w+|void\s+main|new\s+\w+\(|@Override)\b",
        "python": r"(?m)^(?!\s*(import|from\s+\S+\s+import)\b).*\b(def\s+\w+|class\s+\w+|=\s*\S+|if\s+[:\w]|print\s+)",
        "javascript": r"(?m)^(?!\s*(import|require\(|export\s)).*\b(function\s+\w+|const\s+\w+|=>|\(\)\s*=>|console\.log)",
        "php": r"(?m)^(?!\s*(include|require|use)\b).*\b(function\s+\w+|echo\s+\S+|class\s+\w+)",
        "ruby": r"(?m)^(?!\s*(require|load)\b).*\b(class\s+\w+|def\s+\w+|puts\s+\S+)",
        "go": r"(?m)^(?!\s*import\b).*\bfunc\s+main\s*\(|type\s+\w+\s+struct",
        "c#": r"(?m)^(?!\s*using\b).*\b(class\s+\w+|void\s+Main\s*\()",
        "cplusplus": r"(?m)^(?!#include\b).*\b(int\s+main\s*\(|class\s+\w+|void\s+\w+\s*\(.*\)\s*{)",
        "c": r"(?m)^(?!#include\b).*\b(int\s+main\s*\(|void\s+\w+\s*\(.*\)\s*{)",
        "rust": r"(?m)^(?!\s*use\b).*\b(fn\s+main\s*\(|struct\s+\w+|impl\s+\w+)",
        "typescript": r"(?m)^(?!\s*(import|require\(|export\s)).*\b(interface\s+\w+|class\s+\w+|function\s+\w+)",
        "perl": r"(?m)^(?!\s*(use|require)\b).*\b(sub\s+\w+|my\s+\$\w+|print\s+\S+)",
        "shell": r"(?m)^(?!\s*(source|\.)\s).*\b(function\s+\w+|if\s+\[|\$\(|echo\s+\S+)",
        "sql": r"(?i)\b(CREATE\s+TABLE|SELECT\s+\*|INSERT\s+INTO|UPDATE\s+\w+|DELETE\s+FROM)\b",
        "batchfile": r"(?m)^(?!\s*@?call\b).*\b(echo\s+\S+|set\s+\w+|if\s+.*\s+==\s+)",
        "fortran": r"(?mi)^(?!\s*use\b).*\b(program\s+\w+|subroutine\s+\w+|do\s+\d+\s*,\s*\d+)",
        "haskell": r"(?m)^(?!\s*import\b).*\b(main\s*=\s*do|data\s+\w+|putStrLn\s+\S+)",
        "lua": r"(?m)^(?!\s*require\b).*\b(function\s+\w+|local\s+\w+|print\s*\()",
        "powershell": r"(?m)^(?!\s*Import-Module\b).*\b(function\s+\w+|Write-Host\s+\S+|\$\w+\s*=)",
        "visual_basic": r"(?m)^(?!\s*Imports\b).*\b(Module\s+\w+|Sub\s+Main|Class\s+\w+)"
    }

    comment_patterns = {
        'java': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'python': (r'#.*?$', re.MULTILINE),
        'javascript': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'php': (r'//.*?$|#.*?$|/\*.*?\*/|\\/\\/.*?$|#.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'ruby': (r'#.*', re.MULTILINE),
        'go': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'csharp': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'cplusplus': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'c': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'rust': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'typescript': (r'//.*?$|/\*.*?\*/|\\/\\/.*?$|\\/\*.*?\*\\/', re.DOTALL | re.MULTILINE),
        'perl': (r'#.*', re.MULTILINE),
        'shell': (r'#.*', re.MULTILINE),
        'sql': (r'--.*?$|/\*.*?\*/', re.DOTALL),
        'batchfile': (r'^\s*(REM|@REM|::).*', re.MULTILINE | re.IGNORECASE),
        'fortran': (r'!.*', re.MULTILINE),
        'haskell': (r'--.*', re.MULTILINE),
        'lua': (r'--.*?$|--\[\[.*?\]\]', re.DOTALL),
        'powershell': (r'<#.*?#>|#.*', re.DOTALL),
        'visual_basic': (r"'.*", re.MULTILINE),
    }

    if lang in comment_patterns:
        pattern, flags = comment_patterns[lang]
        cleaned_code = re.sub(pattern, '', cleaned_code, flags=flags)
        cleaned_code = clean_empty_lines(cleaned_code)

    if lang == 'fortran':
        cleaned_code = re.sub(r'^[Cc*].*', '', cleaned_code, flags=re.MULTILINE)
    elif lang == 'sql':
        cleaned_code = re.sub(r'/\*.*?\*/', '', cleaned_code, flags=re.DOTALL)
    elif lang == 'python':
        cleaned_code = re.sub(r'^\s*#.*', '', cleaned_code, flags=re.MULTILINE)

    def has_valid_code(text: str, lang: str) -> bool:
        pattern = function_patterns.get(lang)
        if not pattern:
            return len(text.strip()) > 0
        
        if lang == 'batchfile':
            return bool(re.search(r'^\s*@?echo\b|:\w+', text, re.MULTILINE))
        if lang == 'shell':
            return bool(re.search(r'^\s*(if|for|while|case|echo|export|shopt|source)\b', text, re.MULTILINE))
        if lang == 'python':
            if re.search(r'^\s*(def|class)\s+\w+', text, re.MULTILINE):
                return bool(re.search(r'^\s+[^\s#]', text, re.MULTILINE))
            return False
        if lang == 'ruby':
            return bool(re.search(r'(def\s+\w+|class\s+\w+).*?\n\s+[^\s#]', text, re.MULTILINE))
        return bool(re.search(pattern, text, re.DOTALL | re.MULTILINE))

    if not has_valid_code(cleaned_code, lang):
        return ''
    
    cleaned_code = cleaned_code.strip('\ufeff').strip()
    
    if len(cleaned_code) < length_threshold:
        return ''

    return cleaned_code

import os
import random
import datasets
from tqdm import tqdm
from typing import List, Tuple

class CorpusGenerator:
    def __init__(
        self,
        cache_dir: str = None,
    ):
        self.cache_dir = cache_dir

    def _load_corpus(self, corpus_dir: str, doc_length: List[str], external_path: List[str],
                     source_language: str, stop_threshold: int = -1):
        """
        Load availavle documents for a given task from the CoIR-Retrieval dataset.
        """
        lang="Python"
        corpus_list = []

        if corpus_dir is not None and os.path.exists(corpus_dir):
            file_list = os.listdir(corpus_dir)
            random.shuffle(file_list)
            
            for file in file_list:
                flag = False
                if not file.endswith('.jsonl'):
                    flag = False
                for d_length in doc_length:
                    d_length = DocLength[d_length].value
                    if d_length in file:
                        flag = True
                if flag is False:
                    continue
                file_path = os.path.join(corpus_dir, file)
                corpus = datasets.load_dataset('json', data_files=file_path, cache_dir=self.cache_dir)['train']
                for data in tqdm(corpus, desc="Loading corpus"):
                    if source_language is None:
                        lang = os.path.basename(corpus_dir)
                        data['language'] = lang
                    else:
                        data['language'] = source_language
                    
                    text = clean_code(data["text"], data["language"], length_threshold=200)
                    data["text"] = text
                    if text != '':
                        corpus_list.append(data)
                
                if stop_threshold > 0 and len(corpus_list) > stop_threshold:
                    break
                break

        for ep in external_path:
            if os.path.exists(ep):
                corpus = datasets.load_dataset('json', data_files=ep, cache_dir=self.cache_dir)['train']
                for data in tqdm(corpus, desc="Loading corpus"):
                    if source_language is None:
                        lang = os.path.basename(os.path.dirname(ep))
                        data['language'] = lang
                    else:
                        data['language'] = source_language
                    
                    # useful when the text is not present in the data
                    if "text" not in data:
                        data["text"] = data["pos"][0]
                    
                    corpus_list.append(data)
                    text = clean_code(data["text"], lang, length_threshold=200)
                  #  data["text"] = text
                    if text != '':
                        corpus_list.append(data)

        return corpus_list

    def run(
        self,
        num_samples: int = -1,
        max_corpus: int = -1,
        corpus_dir: str = None,
        doc_length: List[str] = ["len_0_500"],
        external_path: List[str] = None,
        source_language: str = None
    ) -> Tuple[List[dict], List[dict]]:
        stop_threshold = max(num_samples * 10, max_corpus * 2)
        corpus_list = self._load_corpus(
            corpus_dir, doc_length, external_path, source_language, stop_threshold
        )

        if num_samples > 0 and num_samples < len(corpus_list):
            small_corpus_list = random.sample(corpus_list, num_samples)
        else:
            small_corpus_list = corpus_list
        
        if max_corpus > 0 and max_corpus < len(corpus_list):
            corpus_list = random.sample(corpus_list, max_corpus)
        else:
            corpus_list = corpus_list

        return small_corpus_list, corpus_list
    


import json
def format_generated_examples(
    file_path: str,
    save_path: str,
    task_type: TaskType
):
    if os.path.exists(save_path):
        return
    
    if not os.path.exists(file_path):
        print("====================================")
        print("Warning: file not found! Maybe need to generate it first.")
        print(f"file_path: {file_path}")
        return
    
    pos_as_input = get_pos_as_input_by_task_type(task_type)
    
    data_list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            data = json.loads(line)
            
            if pos_as_input:
                _input = data["pos"][0]
                _output = data["query"]
            else:
                _input = data["query"]
                _output = data["pos"][0]

            if 'provided' in _input:
                continue
            if len(_input) > 12000 or len(_output) > 12000:
                continue

            data_list.append({
                "input": _input,
                "output": _output
            })
    
    if len(data_list) == 0:
        print("====================================")
        print("Warning: no data found!")
        print(f"file_path: {file_path}")
        return
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)


def main():
    original_gen_examples_dir = "./examples"
    
    formatted_examples_dir = "./filtered_for_generation"
    
    for language in Language:
        for task_type in TaskType:
            if task_type == TaskType.code_translation_retrieval:
                for code_language_pair in CODE_TRANSLATION_RETRIEVAL_PAIRS:
                    code_language, tgt_code_language = code_language_pair
                    
                    file_path = os.path.join(
                        original_gen_examples_dir,
                        language.name, task_type.name, f"{language.name}-{code_language.name}-to-{tgt_code_language.name}-triplets.jsonl"
                    )
                    save_path = os.path.join(
                        formatted_examples_dir,
                        language.name, task_type.name, f"{code_language.name}-to-{tgt_code_language.name}_sample_examples.json"
                    )
                    
                    format_generated_examples(file_path, save_path, task_type)
                    
                for code_language_pair in CODE_TRANSLATION_RETRIEVAL_PAIRS:
                    tgt_code_language, code_language = code_language_pair
                    
                    file_path = os.path.join(
                        original_gen_examples_dir,
                        language.name, task_type.name, f"{language.name}-{code_language.name}-to-{tgt_code_language.name}-triplets.jsonl"
                    )
                    save_path = os.path.join(
                        formatted_examples_dir,
                        language.name, task_type.name, f"{code_language.name}-to-{tgt_code_language.name}_sample_examples.json"
                    )
                    
                    format_generated_examples(file_path, save_path, task_type)
                
            elif task_type == TaskType.text2sql_retrieval:
                file_path = os.path.join(
                    original_gen_examples_dir,
                    language.name, task_type.name, f"{language.name}-sql-triplets.jsonl"
                )
                save_path = os.path.join(
                    formatted_examples_dir,
                    language.name, task_type.name, "sql_sample_examples.json"
                )
                
                format_generated_examples(file_path, save_path, task_type)
            
            elif task_type == TaskType.code_context_retrieval:
                continue
            
            else:
                for code_language in CodeLanguage:
                    if code_language == CodeLanguage.null:
                        continue
                    
                    file_path = os.path.join(
                        original_gen_examples_dir,
                        language.name, task_type.name, f"{language.name}-{code_language.name}-triplets.jsonl"
                    )
                    save_path = os.path.join(
                        formatted_examples_dir,
                        language.name, task_type.name, f"{code_language.name}_sample_examples.json"
                    )
                    
                    format_generated_examples(file_path, save_path, task_type)
    
    print("All done!")



import os
import time
import openai
import random
import tiktoken
import threading
from openai import OpenAI, AzureOpenAI
from typing import Tuple


class LLM:
    def __init__(
        self,
        model: str=r"F:\Models\Qwen\qwen2.5-coder-32b-instruct-q5_k_m.gguf",
        model_type: str = "gguf",
        port: int = 8000,
    ):
        if model_type == "open-source":
            self.client = OpenAI(
                api_key="EMPTY",
                base_url=f"http://localhost:{port}/v1/"
            )
        elif model_type == "azure":
            self.client = AzureOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_API_VERSION", "2024-02-01"),
                azure_endpoint=os.getenv("AZURE_ENDPOINT"),
                azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME", 'gpt-35-turbo')
            )
        elif model_type == "openai":
            self.client = OpenAI(
               # api_key=os.getenv("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"),
                #base_url=os.getenv("OPENAI_BASE_URL", None)
                api_key="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",
                base_url=None
            )
        elif model_type == "gguf":
            # Load local GGUF model using llama-cpp-python
            if not os.path.exists(model):
                raise FileNotFoundError(f"GGUF model not found at {model}")
            
            self.client = Llama(
                model_path=model,
                n_ctx=4096,     # adjust context length if needed
                n_threads=8     # adjust based on your CPU cores
            )
        else:
            raise ValueError("model_type must be one of ['open-source', 'azure', 'openai']")
        
        self.model = model
        self.tokenizer = tiktoken.get_encoding("o200k_base")
    
    def split_text(self, text: str, anchor_points: Tuple[float, float] = (0.4, 0.7)):
        token_ids = self.tokenizer.encode(text)
        anchor_point = random.uniform(anchor_points[0], anchor_points[1])
        split_index = int(len(token_ids) * anchor_point)
        return self.tokenizer.decode(token_ids[:split_index]), self.tokenizer.decode(token_ids[split_index:])
    
    def chat(
        self,
        prompt: str,
        max_tokens: int = 8192,
        logit_bais: dict = None,
        n: int = 1,
        temperature: float = 1.0,
        top_p: float = 0.6,
        repetition_penalty: float = 1.0,
        remove_thinking: bool = True,
        timeout: int = 5000,
    ):
        endure_time = 0
        endure_time_limit = timeout * 2
        
        def create_completion(results):
            try:
                self.client.reset()
                local_prompt=prompt
                print(f"Prompt length: {len(local_prompt)}")
                if len(local_prompt) > 8000: 
                    print(f"⚠️ Truncated long prompt from {len(prompt)} to 8000 characters.") # adjust threshold to around half of n_ctx (≈4096 tokens)
                    local_prompt = local_prompt[:8000]

                completion = self.client.create_chat_completion(
                    model=self.model,
                    messages=[{"role": "user", "content": local_prompt}],
                    max_tokens=max_tokens,
                    logit_bias=logit_bais if logit_bais is not None else {},
                   
                    temperature=temperature,
                    top_p=top_p,
              #      extra_body={'repetition_penalty': repetition_penalty},
               #     timeout=timeout,
                )
                results["content"] = [completion["choices"][0]["message"]["content"]]
               # results["content"] = [x.message.content for x in completion.choices[:n]]
            except openai.BadRequestError as e:
                # The response was filtered due to the prompt triggering Azure OpenAI's content management policy.
                results["content"] = [None for _ in range(n)]
            except openai.APIConnectionError as e:
                results["error"] = f'APIConnectionError({e})'
            except openai.RateLimitError as e:
                results["error"] = f'RateLimitError({e})'
            except Exception as e:
                results["error"] = f"Error: {e}"
        
        while True:
            results = {"content": None, "error": None}
            completion_thread = threading.Thread(target=create_completion, args=(results,))
            completion_thread.start()
            
            start_time = time.time()
            while completion_thread.is_alive():
                elapsed_time = time.time() - start_time
                if elapsed_time > endure_time_limit:
                    print("Completion timeout exceeded. Aborting...")
                    return [None for _ in range(n)]
                time.sleep(1)
            
            # If an error occurred during result processing
            if results["error"]:
                if endure_time >= endure_time_limit:
                    print(f'{results["error"]} - Skip this prompt.')
                    return [None for _ in range(n)]
                print(f"{results['error']} - Waiting for 5 seconds...")
                endure_time += 5
                time.sleep(5)
                continue
            
            content_list = results["content"]
            if remove_thinking:
                content_list = [x.split('</think>')[-1].strip('\n').strip() if x is not None else None for x in content_list]
            return content_list


from typing import Optional, List

import faiss
import numpy as np
from tqdm import tqdm
from FlagEmbedding import FlagModel

def create_index(embeddings: np.ndarray, use_gpu: bool = False):
    index = faiss.IndexFlatIP(len(embeddings[0]))
    embeddings = np.asarray(embeddings, dtype=np.float32)
    if use_gpu:
        co = faiss.GpuMultipleClonerOptions()
        co.shard = True
        co.useFloat16 = True
        index = faiss.index_cpu_to_all_gpus(index, co=co)
    index.add(embeddings)
    return index


def search(
        faiss_index: faiss.Index,
        k: int = 100,
        query_embeddings: Optional[np.ndarray] = None,
        load_path: Optional[str] = None
):
    if query_embeddings is None:
        query_embeddings = np.load(load_path)

    query_size = len(query_embeddings)

    all_scores = []
    all_indices = []

    for i in tqdm(range(0, query_size, 32), desc="Searching"):
        j = min(i + 32, query_size)
        query_embedding = query_embeddings[i: j]
        score, indice = faiss_index.search(query_embedding.astype(np.float32), k=k)
        all_scores.append(score)
        all_indices.append(indice)

    all_scores = np.concatenate(all_scores, axis=0)
    all_indices = np.concatenate(all_indices, axis=0)
    return all_scores, all_indices

def get_top1(
        small_docs,
        encoder_name,
        docs: List[str],
        top: int = 1
):
    encoder = FlagModel(encoder_name, trust_remote_code=True)
    doc_emb = encoder.encode_corpus(docs, max_length=512, batch_size=256)
    small_doc_emb = encoder.encode_corpus(small_docs, max_length=512, batch_size=256)
    faiss_index = create_index(doc_emb, True)
    all_scores, all_indices = search(faiss_index, 1000, small_doc_emb)
    return_docs = []
    for i in range(len(all_indices)):
        return_docs.append([])
        for idx, score in zip(all_indices[i][20:], all_scores[i][20:]):
            d1 = set(docs[idx].split())
            d2 = set(small_docs[i].split())
            if len(d1 & d2) / len(d1 | d2) > 0.95:
                continue
            return_docs[-1].append(docs[idx])
            if len(return_docs[-1]) >= top:
                break
        if len(return_docs[-1]) == 0:
            print(all_indices[i], all_scores[i])
    # print(return_docs)
    del faiss_index
    return return_docs



import random
from tqdm import tqdm
from hashlib import md5
from warnings import warn
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

def compute_md5(text: str):
    return md5(text.encode()).hexdigest()


class TripletGenerator(LLM):
    def __init__(
        self,
        model: str =r"F:\Models\Qwen\qwen2.5-coder-32b-instruct-q5_k_m.gguf",
        model_type: str = "gguf",
        port: int = 8000,
        cache_dir: Optional[str] = None
    ):
        super().__init__(model, model_type, port)
        self.cache_dir = cache_dir
        if self.cache_dir is not None:
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def _gen_for_code_modification_retrieval(
        self,
        task: Task,
        text: str,
        text_b: Optional[str] = None,
        examples: Optional[List[dict]] = None,
        debug_mode: bool = False,
        **kwargs
    ):
        gen_prompt = get_generation_prompt(
            task=task,
            text=text,
            text_b=text_b,
            examples=examples,
            idx=0
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        diff = clean_content(response)
        gen_prompt = get_generation_prompt(
            task=task,
            text=diff,
            examples=examples,
            idx=1
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        modification_instr = clean_content(response)
        
        query = f"{modification_instr}\n```\n{text}\n```"
        pos = text_b
        
        if debug_mode:
            result = {
                "generation_prompt": gen_prompt,
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        else:
            result = {
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        return result
    
    def _gen_for_code_comparison_retrieval(
        self,
        task: Task,
        text: str,
        text_b: Optional[str] = None,
        examples: Optional[List[dict]] = None,
        debug_mode: bool = False,
        **kwargs
    ):
        gen_prompt = get_generation_prompt(
            task=task,
            text=text,
            text_b=text_b,
            examples=examples,
            idx=0
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        diff_question = clean_content(response)
        query = f"{diff_question}\n\nInput Code:\n```\n{text}\n```\n\nOutput Code:\n```\n{text_b}\n```"
        gen_prompt = get_generation_prompt(
            task=task,
            text=query,
            examples=examples,
            idx=1
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        pos = clean_content(response)

        if debug_mode:
            result = {
                "generation_prompt": gen_prompt,
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        else:
            result = {
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        return result
    
    def _gen_for_code_context_retrieval(
        self,
        task: Task,
        text: str,
        anchor_points: Optional[tuple] = (0.4, 0.7),
        **kwargs
    ):
        former_part, latter_part = self.split_text(
            text,
            anchor_points=anchor_points
        )
        result = {
            "prompt": task.task_instruction,
            "query": former_part,
            "pos": [latter_part],
            "neg": []
        }
        return result
    
    @staticmethod
    def _arrange_query_and_pos(task: Task, input_text: str, response: str):
        """
        Arrange the query and positive example based on the task type.
        
        Args:
        - task: Task
        - input_text: str
        - response: str
        
        Returns:
        - query: str
        - pos: str
        """
        # TODO: support more task types, including some special task types.
        if task.main_task_type in ["text2code", "hybrid"]:
            query = clean_content(response)
            pos = input_text
        else:
            query = input_text
            pos = clean_content(response)
        return query, pos
    
    def _gen_for_normal_task(
        self,
        task: Task,
        text: str,
        examples: Optional[List[dict]] = None,
        debug_mode: bool = False,
        **kwargs
    ):
        gen_prompt = get_generation_prompt(
            task=task,
            text=text,
            examples=examples
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        
        # Arrange the query and positive example based on the task type.
        query, pos = self._arrange_query_and_pos(
            task=task,
            input_text=text,
            response=response
        )
        
        if debug_mode:
            result = {
                "generation_prompt": gen_prompt,
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": [],
                "response": response
            }
        else:
            result = {
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        return result
    
    def _gen_for_bug_desc_retrieval(
        self,
        task: Task,
        text: str,
        examples: Optional[List[dict]] = None,
        debug_mode: bool = False,
        **kwargs
    ):
        gen_prompt = get_generation_prompt(
            task=task,
            text=text,
            examples=examples,
            idx=0
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        if response is None:
            raise ValueError("Response is None.")
        buggy_code = response
        gen_prompt = get_generation_prompt(
            task=task,
            text=buggy_code,
            examples=examples,
            idx=1
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        query = clean_content(response)
        pos = text
        
        if debug_mode:
            result = {
                "generation_prompt": gen_prompt,
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        else:
            result = {
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        return result
    
    def _gen_for_two_step_not_use_last(
        self,
        task: Task,
        text: str,
        examples: Optional[List[dict]] = None,
        debug_mode: bool = False,
        reverse_query_pos: bool = False,
        **kwargs
    ):
        gen_prompt = get_generation_prompt(
            task=task,
            text=text,
            idx=0
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        query = clean_content(response)
        gen_prompt = get_generation_prompt(
            task=task,
            text=query,
            examples=examples,
            idx=1
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        pos = clean_content(response)
        if reverse_query_pos:
            query, pos = pos, query

        if debug_mode:
            result = {
                "generation_prompt": gen_prompt,
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        else:
            result = {
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        return result

    def _gen_for_two_step_use_last(
        self,
        task: Task,
        text: str,
        examples: Optional[List[dict]] = None,
        debug_mode: bool = False,
        reverse_query_pos: bool = False,
        **kwargs
    ):
        gen_prompt = get_generation_prompt(
            task=task,
            text=text,
            idx=0
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        query = clean_content(response) + f"\n```\n{text}\n```"
        gen_prompt = get_generation_prompt(
            task=task,
            text=query,
            examples=examples,
            idx=1
        )
        response = self.chat(gen_prompt, **kwargs)[0]
        pos = clean_content(response)
        if reverse_query_pos:
            query, pos = pos, query

        if debug_mode:
            result = {
                "generation_prompt": gen_prompt,
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        else:
            result = {
                "prompt": task.task_instruction,
                "query": query,
                "pos": [pos],
                "neg": []
            }
        return result

    def generate_triplets(
        self,
        data: dict,
        task: Task,
        examples_pool: Optional[List[dict]] = None,
        num_examples: int = 3,
        debug_mode: bool = False,
        **kwargs
    ):
        kwargs["remove_thinking"] = not debug_mode
        
        result_list = []
        
        examples = None
        if examples_pool is not None:
            examples = random.sample(examples_pool, min(num_examples, len(examples_pool)))

        try:
            if task.task_type in SPECIAL_TASK_STEPS:
                text = data["text"]
                
                if task.task_type == TaskType.code_modification_retrieval:
                    text_b = data["similar"][0]
                    
                    result = self._gen_for_code_modification_retrieval(
                        task=task,
                        text=text,
                        text_b=text_b,
                        examples=examples,
                        debug_mode=debug_mode
                    )
                elif task.task_type == TaskType.code_comparison_retrieval:
                    text_b = data["similar"][0]
                    
                    result = self._gen_for_code_comparison_retrieval(
                        task=task,
                        text=text,
                        text_b=text_b,
                        examples=examples,
                        debug_mode=debug_mode
                    )
                elif task.task_type == TaskType.bug_desc_retrieval:
                    result = self._gen_for_bug_desc_retrieval(
                        task=task,
                        text=text,
                        examples=examples,
                        debug_mode=debug_mode
                    )
                elif task.task_type in [
                    # cf - updated
                    TaskType.code_issue_discussion_retrieval,
                    TaskType.code_version_update_retrieval,
                    TaskType.code_bug_fix_example_retrieval,
                ]:
                    result = self._gen_for_two_step_not_use_last(
                        task=task,
                        text=text,
                        examples=examples,
                        debug_mode=debug_mode,
                        reverse_query_pos=False
                    )
                elif task.task_type in [
                    # cf - updated
                    TaskType.code_refactoring_pattern_retrieval,
                    TaskType.code_style_guideline_example_retrieval,
                    TaskType.code_migration_retrieval,
                    # jl - updated
                    TaskType.code_optimization_hybrid_retrieval,
                    TaskType.code_best_practices_retrieval,
                    TaskType.security_vulnerability_fix_retrieval,
                ]:
                    result = self._gen_for_two_step_use_last(
                        task=task,
                        text=text,
                        examples=examples,
                        debug_mode=debug_mode,
                        reverse_query_pos=False
                    )
                else:
                    raise NotImplementedError(f"Task type {task.task_type} not implemented.")
            elif task.task_type == TaskType.code_context_retrieval:
                text = data["text"]
                
                result = self._gen_for_code_context_retrieval(
                    task=task,
                    text=text,
                    **kwargs
                )
                # NOTE: no need to do quality control for code context retrieval task
                result_list.append(result)
                return result_list
            else:
                text = data["text"]
                
                result = self._gen_for_normal_task(
                    task=task,
                    text=text,
                    examples=examples,
                    debug_mode=debug_mode,
                    **kwargs
                )
            
            qc_prompt = get_quality_control_prompt(
                task=task,
                query=result["query"],
                pos=result["pos"][0]
            )
            response = self.chat(qc_prompt, **kwargs)[0]
            judge = clean_content(response)
            # print(response, judge)
            if "1" in judge:
                if debug_mode:
                    result["judge"] = judge
                    result["judge_response"] = response
                result_list.append(result)
            else:
                if debug_mode:
                    result["judge"] = judge
                    result["judge_response"] = response
                    result_list.append(result)
        except Exception as e:
            warn(f"Error: {e}")
        
        return result_list

    def gen_hard_negatives(self, result: dict, task: Task, num_negatives: int = 7, **kwargs):
        gen_hard_neg_prompt = get_gen_hard_neg_prompt(
            task=task,
            query=result["query"],
            pos=result["pos"][0]
        )
        response_list = self.chat(gen_hard_neg_prompt, n=num_negatives, **kwargs)
        for response in response_list:
            if response is None:
                continue
            hard_neg = clean_content(response)
            result["neg"].append(hard_neg)
        result["neg"] = list(set(result["neg"]))
        return result

    def run_single(
        self,
        data: dict,
        task: Task,
        examples_pool: Optional[List[dict]] = None,
        num_examples: int = 3,
        debug_mode: bool = False,
        gen_hard_neg: bool = True,
        num_negatives: int = 7,
        **kwargs
    ):
        result_list = []

        docid = compute_md5(data["text"])
        if self.cache_dir is not None:
            gen_data_cache_path = os.path.join(self.cache_dir, f"{docid}.json")
            if os.path.exists(gen_data_cache_path):
                with open(gen_data_cache_path, "r", encoding="utf-8") as f:
                    result_list = json.load(f)
                
                if len(result_list) > 0:
                    if gen_hard_neg:
                        for i in range(len(result_list)):
                            if len(result_list[i]["neg"]) == 0:
                                result_list[i] = self.gen_hard_negatives(
                                    result=result_list[i],
                                    task=task,
                                    num_negatives=num_negatives,
                                    **kwargs
                                )
                        # overwrite the cache file
                        with open(gen_data_cache_path, "w", encoding="utf-8") as f:
                            json.dump(result_list, f, indent=4, ensure_ascii=False)
                    return result_list

        triplets = self.generate_triplets(
            data,
            task=task,
            examples_pool=examples_pool,
            num_examples=num_examples,
            debug_mode=debug_mode,
            **kwargs
        )
        if len(triplets) == 0:
            return []
        
        result = triplets[0]
        if debug_mode:
            result["docid"] = docid
        
        if gen_hard_neg:
            result = self.gen_hard_negatives(
                result,
                task=task,
                num_negatives=num_negatives,
                **kwargs
            )
        
        result_list.append(result)
        
        if self.cache_dir is not None:
            gen_data_cache_path = os.path.join(self.cache_dir, f"{docid}.json")
            with open(gen_data_cache_path, "w", encoding="utf-8") as f:
                json.dump(result_list, f, indent=4, ensure_ascii=False)
        
        return result_list

    def run(
        self,
        positives: List[dict],
        task_type: str,
        language: str = "en",
        code_language: str = "python",
        tgt_code_language: Optional[str] = None,
        examples_pool: Optional[List[dict]] = None,
        num_examples: int = 3,
        tqdm_desc: str = "Generating triplets",
        debug_mode: bool = False,
        gen_hard_neg: bool = True,
        num_negatives: int = 7,
        thread_count: int = 1,
        **kwargs
    ):
        task = get_task(
            task_type=task_type,
            language=language,
            code_language=code_language,
            tgt_code_language=tgt_code_language
        )
        
        result_list = []

        def process_positive(positive):
            return self.run_single(
                data=positive,
                task=task,
                examples_pool=examples_pool,
                num_examples=num_examples,
                debug_mode=debug_mode,
                gen_hard_neg=gen_hard_neg,
                num_negatives=num_negatives,
                **kwargs
            )
        # Use thread pool for parallel processing with tqdm progress bar.
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            results = list(tqdm(executor.map(
                process_positive,
                positives
            ), total=len(positives), desc=tqdm_desc))

        # Collect results into result_list.
        for res in results:
            if isinstance(res, list):
                result_list.extend(res)
            else:
                result_list.append(res)
        # result_list.extend(results)

        return result_list

    def run_for_gen_neg(
        self,
        pairs: List[dict],
        task_type: str,
        language: str = "en",
        code_language: str = "python",
        tgt_code_language: Optional[str] = None,
        examples_pool: Optional[List[dict]] = None,
        num_examples: int = 3,
        tqdm_desc: str = "Generating triplets",
        debug_mode: bool = False,
        gen_hard_neg: bool = True,
        num_negatives: int = 7,
        thread_count: int = 1,
        **kwargs
    ):
        task = get_task(
            task_type=task_type,
            language=language,
            code_language=code_language,
            tgt_code_language=tgt_code_language
        )
        
        result_list = []

        def gen_single_negative(pair):
            result = self.gen_hard_negatives(
                pair,
                task=task,
                num_negatives=num_negatives,
                **kwargs
            )
            return [result]

        # Use thread pool for parallel processing with tqdm progress bar.
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            results = list(tqdm(executor.map(
                gen_single_negative,
                pairs
            ), total=len(pairs), desc=tqdm_desc))

        # Collect results into result_list.
        for res in results:
            if isinstance(res, list):
                result_list.extend(res)
            else:
                result_list.append(res)
        # result_list.extend(results)

        return result_list


import time
import gc
import torch
import argparse
import random
from hashlib import md5
import multiprocessing as mp
from typing import List, Optional


def compute_md5(text: str):
    return md5(text.encode()).hexdigest()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--task_type',
        type=str,
        default='text2sql_retrieval',
        help='The task type to generate data for',
        choices=[t.name for t in TaskType]
    )
    parser.add_argument(
        '--code_language',
        type=str,
        default='sql',
        help='addffeedda',
        choices=[c.name for c in CodeLanguage]
    )
    parser.add_argument(
        '--corpus_root',
        type=str,
        default=r"F:\movies",
        help='The root directory of the corpus data.'
    )
    parser.add_argument(
        '--save_dir',
        type=str,
        default=r"Downloads",
        help='The path to save the generated data'
    )
    parser.add_argument(
        '--examples_dir',
        type=str,
        default=None,
        help='The path to the examples directory. If not None, the examples will be used for few-shot generation.'
    )
    parser.add_argument(
        '--num_examples',
        type=int,
        default=3,
        help='The number of examples to use for few-shot generation. Default: 3'
    )
    parser.add_argument(
        '--cache_dir',
        type=str,
        default=None,
        help='The cache directory'
    )
    parser.add_argument(
        '--language',
        type=str,
        default='en',
        help='The language to generate for. ISO 639-1 code. Default: en',
        choices=[l.name for l in Language]
    )
    parser.add_argument(
        '--tgt_code_language',
        type=str,
        default='sql',
        help='The target code language to generate code translations for.',
        choices=[c.name for c in CodeLanguage]
    )
    parser.add_argument(
        '--num_samples',
        type=int,
        default=-1,
        help='The number of examples to use for generation. Default: -1. Use all available examples.'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=r"F:\Models\Qwen\qwen2.5-coder-32b-instruct-q5_k_m.gguf",
        help='The model to use for generation. Default: Qwen2.5-72B-Instruct'
    )
    parser.add_argument(
        '--model_type',
        type=str,
        default='gguf',
        help='The type of model to use for generation. Default: open-source',
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='The port for vllm.'
    )
    parser.add_argument(
        '--num_processes',
        type=int,
        default=1,
        help='The number of processes to use for generation. Default: 1'
    )
    parser.add_argument(
        '--doc_length',
        type=str,
        default="text2sql_retrieval_10_samples.json",
        help='The corpus length used to load dataset. Default: len_0_500'
    )
    parser.add_argument(
        '--external_path',
        type=str,
        default=r"F:\movies\text2sql_retrieval_10_samples.json",
        help='The corpus length used to load dataset. Default: len_0_500'
    )
    parser.add_argument(
        '--sim_model_name',
        type=str,
        default=None,
        help='The language of source corpus.'
    )
    parser.add_argument(
        '--max_corpus',
        type=int,
        default=500000,
        help='The max num of corpus to load.'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Whether to overwrite the existing data.'
    )
    parser.add_argument(
        '--debug_mode',
        action='store_true',
        help='Whether to open debug mode.'
    )
    parser.add_argument(
        '--gen_hard_neg',
       
        action='store_true',
        help='Whether to generate hard negatives.'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for generating triplets using the same positive. Default: 42'
    )
    args = parser.parse_args()
    return args


def gen_triplets(
    model: str,
    model_type: str,
    port: int,
    positives: List[dict],
    task_type: str,
    language: str,
    code_language: str,
    tgt_code_language: str,
    examples_pool: Optional[List[dict]] = None,
    num_examples: int = 3,
    tqdm_desc: str = "Generating triplets",
    thread_count: int = 1,
    gen_cache_dir: Optional[str] = None,
    debug_mode: bool = False,
    gen_hard_neg: bool = True,
):
    triplet_generator = TripletGenerator(model=model, cache_dir=gen_cache_dir)
    triplets = triplet_generator.run(
        positives=positives,
        task_type=task_type,
        language=language,
        code_language=code_language,
        tgt_code_language=tgt_code_language,
        examples_pool=examples_pool,
        num_examples=num_examples,
        tqdm_desc=tqdm_desc,
        thread_count=thread_count,
        debug_mode=debug_mode,
        gen_hard_neg=gen_hard_neg,
        num_negatives=NUM_HARD_NEGATIVES,
    )
    return triplets


def get_save_path(
    save_dir: str,
    task_type: str,
    language: str,
    code_language: str,
    tgt_code_language: str # Optional[str] = None
):
    save_dir = os.path.join(save_dir, language, task_type)
    if tgt_code_language is not None:
        file_name = f"{language}-{code_language}-to-{tgt_code_language}-triplets.jsonl"
    else:
        file_name = f"{language}-{code_language}-triplets.jsonl"
    save_path = os.path.join(save_dir, file_name)
    os.makedirs(save_dir, exist_ok=True)
    return save_path


def save_triplets(
    triplets: list,
    save_dir: str,
    task_type: str,
    language: str,
    code_language: str,
    tgt_code_language: Optional[str] = None
):
    if len(triplets) == 0:
        print(f"No triplets to save: {task_type} | {language} | {code_language} | {tgt_code_language}")
        return
    
    save_path = get_save_path(save_dir, task_type, language, code_language, tgt_code_language)
    query_md5s = set()
    pos_md5s = set()
    old_triplets = []
    if os.path.exists(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                triplet = json.loads(line)
                old_triplets.append(triplet)
                query_md5s.add(compute_md5(triplet['query']))
                pos_md5s.add(compute_md5(triplet['pos'][0]))

    with open(save_path, 'w', encoding='utf-8') as f:
        for triplet in old_triplets:
            f.write(json.dumps(triplet, ensure_ascii=False) + '\n')
        
        for triplet in triplets:
            _query_md5 = compute_md5(triplet['query'])
            _pos_md5 = compute_md5(triplet['pos'][0])
            if _query_md5 in query_md5s or _pos_md5 in pos_md5s:
                continue
            f.write(json.dumps(triplet, ensure_ascii=False) + '\n')
    print(f"Triplets saved to {save_path}")


def main(args):
    # set seed
    seed = args.seed
    if seed is not None:
        print(f"------------------- Seed set to {seed} -------------------")
        random.seed(seed)
    
    model = args.model
    model_type = args.model_type
    port = args.port

    num_samples = args.num_samples
    
    task_type = args.task_type
    language = args.language
    code_language = args.code_language
    tgt_code_language = args.tgt_code_language

    corpus_root = args.corpus_root
    corpus_dir = os.path.join(corpus_root, code_language)
    doc_length = args.doc_length.split()
    external_path = args.external_path.split()

    save_dir = args.save_dir
    cache_dir = args.cache_dir
    num_processes = min(args.num_processes, int(mp.cpu_count() * 0.8))
    overwrite = args.overwrite
    debug_mode = args.debug_mode
    gen_hard_neg = args.gen_hard_neg
    gen_hard_neg=True
    save_path = get_save_path(save_dir, task_type, language, code_language, tgt_code_language)
    # if os.path.exists(save_path) and not overwrite:
        # data = []
        # with open(save_path) as f:
        #     for line in f:
        #         data.append(json.loads(line))
        # if len(data) >= num_samples * 0.8:
        #     print(f"Triplets already exist at {save_path}. Skipping generation.")
        #     return
        # else:
        #     print(f"Triplets already exist at {save_path}. But samples is really small, continue generation.")
        #     num_samples = int((num_samples - len(data)) * 1.25)  # consider the filtered samples

    corpus_generator = CorpusGenerator(cache_dir)

    examples_dir = args.examples_dir
    num_examples = args.num_examples
    if examples_dir is not None:
        # if task_type in ["single_turn_code_qa", "multi_turn_code_qa"]:
        #     examples_path = os.path.join(examples_dir, language, task_type, "sample_examples.json")
        if task_type in ["code_translation_retrieval"]:
            examples_path = os.path.join(examples_dir, language, task_type,
                                         f"{code_language}-to-{tgt_code_language}_sample_examples.json")
        else:
            examples_path = os.path.join(examples_dir, language, task_type, f"{code_language}_sample_examples.json")
        try:
            with open(examples_path, 'r', encoding='utf-8') as f:
                examples_pool = json.load(f)
                examples_pool = random.sample(examples_pool,
                                              min(30, len(examples_pool)))   # sample 30 examples for few-shot generation
        except:
            print(f'Error for loading examples from {examples_path}')
            examples_pool = None
    else:
        examples_pool = None

    positives, large_positives = corpus_generator.run(
        num_samples=num_samples,
        max_corpus=args.max_corpus,
        corpus_dir=corpus_dir,
        doc_length=doc_length,
        external_path=external_path,
        source_language=code_language
    )

    if task_type in ["code_modification_retrieval", "code_comparison_retrieval"]:
        top1_docs = get_top1([e['text'] for e in positives], args.sim_model_name, [e['text'] for e in large_positives])
        for i in range(len(top1_docs)):
            positives[i]['similar'] = top1_docs[i]
        gc.collect()
        torch.cuda.empty_cache()

    print("=================== Generate training data ===================")
    print(f'Task Type: {task_type} | Language: {language} | Code Language: {code_language} | Target Code Language: {tgt_code_language}')
    start_time = time.time()
    
    triplets = gen_triplets(
        model=model,
        model_type=model_type,
        port=port,
        positives=positives,
        task_type=task_type,
        language=language,
        code_language=code_language,
        tgt_code_language=tgt_code_language,
        examples_pool=examples_pool,
        num_examples=num_examples,
        thread_count=num_processes,
        gen_cache_dir=os.path.join(save_dir, language, task_type, "gen_cache_dir"),
        debug_mode=debug_mode,
        gen_hard_neg=gen_hard_neg,
    )
    print("positives:", positives)
    print("✅ Generated triplets:", triplets)
    save_triplets(
        triplets=triplets,
        save_dir=save_dir,
        task_type=task_type,
        language=language,
        code_language=code_language,
        tgt_code_language=tgt_code_language
    )
    end_time = time.time()
    print("=============================================================")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print("=============================================================")
    print("DONE!")


if __name__ == "__main__":
    args = get_args()
    main(args)