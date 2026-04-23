import { Task, TaskState, TaskMessage, Artifact, SSEEvent } from './schema';

export class EventBus {
  private listeners: Map<string, Set<(event: SSEEvent) => void>> = new Map();

  subscribe(taskId: string, callback: (event: SSEEvent) => void): () => void {
    if (!this.listeners.has(taskId)) {
      this.listeners.set(taskId, new Set());
    }
    this.listeners.get(taskId)!.add(callback);

    return () => {
      this.listeners.get(taskId)?.delete(callback);
    };
  }

  async publish(event: any): Promise<void> {
    const taskId = event.taskId;
    const listeners = this.listeners.get(taskId);
    if (listeners) {
      for (const callback of listeners) {
        try {
          callback(event);
        } catch (e) {
          console.error(`[EventBus] Listener error for task ${taskId}:`, e);
        }
      }
    }
  }
}

export class TaskStore {
  private tasks: Map<string, Task> = new Map();

  async getTask(taskId: string): Promise<Task | undefined> {
    return this.tasks.get(taskId);
  }

  async setTask(task: Task): Promise<void> {
    this.tasks.set(task.id, task);
  }

  async deleteTask(taskId: string): Promise<void> {
    this.tasks.delete(taskId);
  }

  async updateTask(taskId: string, updates: Partial<Task>): Promise<Task | undefined> {
    const task = this.tasks.get(taskId);
    if (task) {
      const updated = { ...task, ...updates, updated_at: new Date().toISOString() };
      this.tasks.set(taskId, updated);
      return updated;
    }
    return undefined;
  }

  async listTasks(filter?: {
    contextId?: string;
    state?: TaskState;
    client_agent_id?: string;
  }): Promise<Task[]> {
    let tasks = Array.from(this.tasks.values());
    
    if (filter?.contextId) {
      tasks = tasks.filter(t => t.contextId === filter.contextId);
    }
    if (filter?.state) {
      tasks = tasks.filter(t => t.status.state === filter.state);
    }
    if (filter?.client_agent_id) {
      tasks = tasks.filter(t => t.client_agent_id === filter.client_agent_id);
    }
    
    return tasks.sort((a, b) => 
      new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    );
  }
}
