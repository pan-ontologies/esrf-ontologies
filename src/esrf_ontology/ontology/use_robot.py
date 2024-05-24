import subprocess


def run_robot_reasoner(input_ontology="/home/koumouts/code/esrf-ontology/src/esrf_ontology/ontology/esrf_ontology.owl", output_ontology="robot_esrf_ontology.owl"):
    # Define the ROBOT jar file path
    robot_jar = "/users/koumouts/code/robot/robot.jar"

    # Build the ROBOT reason command
    command = [
        "java", "-jar", robot_jar, "reason",
        "--input", input_ontology,
        "--output", output_ontology
    ]

    try:
        # Run the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Reasoning completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during reasoning:", e)
        print(e.stderr)


# if __name__ == "__main__":
#     # Path to the input ontology file
#     input_ontology = "esrf_ontology.owl"
#     # Path to the output ontology file
#     output_ontology = "robot_esrf_ontology.owl"

#     # Run the reasoner
#     run_robot_reasoner(input_ontology, output_ontology)
