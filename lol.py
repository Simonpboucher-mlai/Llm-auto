def autonomous_step_reasoning(
    question,
    model="gpt-4",
    temperature=0.7
):
    """
    Fonction de raisonnement où le modèle :
    1. Détermine de façon autonome les étapes nécessaires
    2. Exécute chaque étape séquentiellement
    3. Maintient l'historique complet entre les étapes
    """
    
    print(f"Question initiale : {question}\n")
    print("=" * 80 + "\n")

    # 1. Détermination des étapes nécessaires
    planning_prompt = """Pour répondre à la question suivante, détermine les étapes nécessaires de façon autonome.

Question : {question}

Définis :
1. Le nombre d'étapes nécessaires
2. Une description précise de chaque étape
3. L'objectif spécifique de chaque étape

Format de réponse STRICT:
NOMBRE D'ÉTAPES: [nombre]

PLAN DÉTAILLÉ:
1. [Nom de l'étape 1]
   Objectif: [objectif précis]
   Tâche: [description détaillée de ce qui doit être fait]

2. [Nom de l'étape 2]
   Objectif: [objectif précis]
   Tâche: [description détaillée de ce qui doit être fait]

[etc. pour chaque étape]

JUSTIFICATION:
[Explique pourquoi ces étapes sont nécessaires et dans cet ordre]"""

    print("Planification des étapes...")
    planning_messages = [
        {
            "role": "system",
            "content": "Tu es un expert en planification et décomposition de problèmes complexes."
        },
        {
            "role": "user",
            "content": planning_prompt.format(question=question)
        }
    ]

    plan_response = generate_openai_response(
        model=model,
        messages=planning_messages,
        temperature=temperature
    )
    plan = plan_response.split("**Assistant:**\n\n")[1].strip()
    
    print("\nPlan établi :")
    print("-" * 20)
    print(plan)
    print("-" * 20 + "\n")

    # 2. Exécution séquentielle des étapes
    execution_history = [
        {
            "role": "system",
            "content": "Tu es un assistant expert qui exécute méticuleusement chaque étape du raisonnement."
        },
        {
            "role": "user",
            "content": f"Question initiale : {question}\n\nPlan d'exécution :\n{plan}"
        }
    ]

    # Extraire le nombre d'étapes du plan
    number_of_steps = int(plan.split("NOMBRE D'ÉTAPES:")[1].split("\n")[0].strip())
    
    print(f"\nExécution des {number_of_steps} étapes...\n")

    for step in range(1, number_of_steps + 1):
        print(f"\nExécution de l'étape {step}/{number_of_steps}")
        print("-" * 40)

        execution_prompt = f"""En tenant compte de tout l'historique précédent, exécute l'étape {step}.

Historique complet:
{' '.join([msg['content'] for msg in execution_history if msg['role'] == 'assistant'])}

Format de réponse:
ÉTAPE {step}:
[Nom de l'étape]

EXÉCUTION:
[Réalisation détaillée de l'étape]

RÉSULTATS:
[Conclusions ou résultats de cette étape]"""

        execution_messages = execution_history + [
            {
                "role": "user",
                "content": execution_prompt
            }
        ]

        step_response = generate_openai_response(
            model=model,
            messages=execution_messages,
            temperature=temperature
        )
        step_result = step_response.split("**Assistant:**\n\n")[1].strip()
        
        print("\nRésultat de l'étape :")
        print(step_result)
        print("-" * 40)

        # Ajouter le résultat à l'historique
        execution_history.append({
            "role": "assistant",
            "content": step_result
        })

    # 3. Synthèse finale
    print("\nGénération de la synthèse finale...")
    
    synthesis_prompt = """En te basant sur toutes les étapes exécutées, génère une synthèse finale.

Question initiale : {question}

Historique complet des étapes :
{history}

Format de réponse:
SYNTHÈSE FINALE:
[Synthèse complète intégrant les résultats de toutes les étapes]

CONCLUSION:
[Conclusion finale répondant à la question initiale]"""

    synthesis_messages = [
        {
            "role": "system",
            "content": "Tu es un expert en synthèse et intégration de résultats complexes."
        },
        {
            "role": "user",
            "content": synthesis_prompt.format(
                question=question,
                history=' '.join([msg['content'] for msg in execution_history if msg['role'] == 'assistant'])
            )
        }
    ]

    final_response = generate_openai_response(
        model=model,
        messages=synthesis_messages,
        temperature=temperature
    )
    final_result = final_response.split("**Assistant:**\n\n")[1].strip()

    # Affichage final
    final_output = "# Résultat du raisonnement par étapes\n\n"
    final_output += f"**Question initiale :** {question}\n\n"
    final_output += "## Plan d'exécution\n\n"
    final_output += plan + "\n\n"
    final_output += "## Synthèse finale\n\n"
    final_output += final_result

    display(Markdown(final_output))

    return {
        "plan": plan,
        "execution_history": execution_history,
        "final_synthesis": final_result
    }


question = "Comment l'intelligence artificielle pourrait-elle contribuer à résoudre la crise climatique?"
result = autonomous_step_reasoning(question)
