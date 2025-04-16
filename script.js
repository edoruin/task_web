document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("task-form");
    const taskList = document.getElementById("task-list");
    let tasks = JSON.parse(localStorage.getItem("tasks")) || [];
  
    const renderTasks = () => {
      taskList.innerHTML = "";
      tasks.forEach((task, index) => {
        const li = document.createElement("li");
        li.className = "task" + (task.completed ? " completed" : "");
        li.innerHTML = `
          <div>
            <strong>${task.title}</strong><br>
            <small>${task.desc}</small>
          </div>
          <div>
            <button onclick="toggleTask(${index})">✔</button>
            <button onclick="deleteTask(${index})">🗑️</button>
          </div>
        `;
        taskList.appendChild(li);
      });
    };
  
    const saveTasks = () => {
      localStorage.setItem("tasks", JSON.stringify(tasks));
    };
  
    window.toggleTask = (index) => {
      tasks[index].completed = !tasks[index].completed;
      saveTasks();
      renderTasks();
    };
  
    window.deleteTask = (index) => {
      tasks.splice(index, 1);
      saveTasks();
      renderTasks();
    };
  
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const title = document.getElementById("task-title").value.trim();
      const desc = document.getElementById("task-desc").value.trim();
      if (title) {
        tasks.push({ title, desc, completed: false });
        saveTasks();
        renderTasks();
        form.reset();
      }
    });
  
    renderTasks();
  });
  