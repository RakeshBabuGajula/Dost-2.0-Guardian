import { OperationsDataProvider, OperationalDataMode } from '../../types/backend';
import { simulationDataProvider } from './SimulationDataProvider';
import { BackendDataProvider } from './BackendDataProvider';

class OperationsManager {
  private activeProvider: OperationsDataProvider;
  private backendProvider: BackendDataProvider | null = null;
  private mode: OperationalDataMode;

  constructor() {
    const envMode = (import.meta.env.VITE_DATA_MODE || 'simulation') as OperationalDataMode;
    this.mode = envMode;

    if (this.mode === 'backend') {
      this.backendProvider = new BackendDataProvider();
      this.activeProvider = this.backendProvider;
    } else {
      this.activeProvider = simulationDataProvider;
    }
  }

  public getProvider(): OperationsDataProvider {
    return this.activeProvider;
  }

  public setMode(mode: OperationalDataMode): void {
    if (this.mode === mode) return;

    this.mode = mode;
    if (mode === 'backend') {
      if (!this.backendProvider) {
        this.backendProvider = new BackendDataProvider();
      }
      this.activeProvider = this.backendProvider;
    } else {
      this.activeProvider = simulationDataProvider;
    }
  }

  public getMode(): OperationalDataMode {
    return this.mode;
  }
}

export const operationsManager = new OperationsManager();
