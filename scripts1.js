function addTask() {
    const taskName = document.getElementById('taskName').value;
    const taskCategory = document.getElementById('taskCategory').value;
    const taskDueDate = document.getElementById('taskDueDate').value;
    const taskPriority = document.getElementById('taskPriority').value;

    if (taskName.trim() === '') {
        alert('Task name cannot be empty.');
        return;
    }

    const taskList = document.getElementById('taskList');
    const listItem = document.createElement('li');

    const taskInfo = document.createElement('div');
    taskInfo.className = 'task-info';

    const taskTitle = document.createElement('span');
    taskTitle.textContent = taskName;
    taskInfo.appendChild(taskTitle);

    if (taskCategory) {
        const taskCat = document.createElement('span');
        taskCat.textContent = `Category: ${taskCategory}`;
        taskInfo.appendChild(taskCat);
    }

    if (taskDueDate) {
        const taskDate = document.createElement('span');
        taskDate.textContent = `Due: ${taskDueDate}`;
        taskInfo.appendChild(taskDate);
    }

    const taskPri = document.createElement('span');
    taskPri.className = `task-priority ${taskPriority.toLowerCase()}`;
    taskPri.textContent = `Priority: ${taskPriority}`;
    taskInfo.appendChild(taskPri);

    const taskActions = document.createElement('div');
    taskActions.className = 'task-actions';

    const completeButton = document.createElement('button');
    completeButton.textContent = 'Complete';
    completeButton.onclick = () => {
        taskList.removeChild(listItem);
    };
    taskActions.appendChild(completeButton);

    listItem.appendChild(taskInfo);
    listItem.appendChild(taskActions);
    taskList.appendChild(listItem);

    document.getElementById('taskName').value = '';
    document.getElementById('taskCategory').value = '';
    document.getElementById('taskDueDate').value = '';
    document.getElementById('taskPriority').value = 'Low';
}
