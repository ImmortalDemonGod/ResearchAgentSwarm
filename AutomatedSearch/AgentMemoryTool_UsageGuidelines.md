# Agent Memory Tool Usage Guidelines

The Agent Memory Tool is an essential component within our AI agency for storing, retrieving, and managing information specific to each AI agent. Proper utilization of this tool is crucial for maintaining continuity and effectiveness in our projects.

## Accessing the Memory
- Use the case-sensitive 'Agent Name' to target the correct agent's memory. Incorrect capitalization will result in a 'Key not found' error.
- Specify the 'Read Key' with exact casing and spelling as the memory keys are also case-sensitive.

## Storing Memory
- To store information, use the 'Write Data' parameter with the 'Agent Name'.
- Data should be structured and named clearly to avoid confusion and ease retrieval.

## Retrieval of Information
- Retrieve information by providing the 'Read Key' corresponding to the data you wish to access.
- Ensure the key exactly matches the one used when the data was stored.

## Best Practices
- Maintain a consistent naming convention for keys across the agency.
- Regularly update the memory with relevant and current data.
- Before storing, ensure that the data is accurate and complete.
- Avoid the use of ambiguous or overly broad terms for keys.

By adhering to these guidelines, we can ensure that the Agent Memory Tool is used effectively and that all agents can rely on accurate information when needed.

*Note: In case of persistent issues with memory access, consider verifying the keys listed in 'all_agents_keys' versus actual key usage and consult with technical support if discrepancies are found.*