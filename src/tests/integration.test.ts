import 'fake-indexeddb/auto';
import { storeOfflineEvent, getPendingOfflineEvents, offlineDb } from '../services/offline/offlineStore';
import { offlineSyncService } from '../services/offline/syncService';
import { simulationDataProvider } from '../services/providers/SimulationDataProvider';

function assert(condition: boolean, message: string) {
  if (!condition) {
    console.error(`❌ TEST FAILED: ${message}`);
    process.exit(1);
  } else {
    console.log(`  ✓ ${message}`);
  }
}

async function runIntegrationSuite() {
  console.log('🚀 Running DOST Guardian 2.0 Application Foundation Integration Suite...\n');

  // 1. Simulation Provider Abstraction
  console.log('Testing 1: Simulation Data Provider Abstraction');
  const simState = simulationDataProvider.getState();
  assert(simState.mode === 'simulation', 'Mode set to simulation');
  assert(simState.workers.length > 0, 'Workers roster loaded');
  assert(simState.trains.length > 0, 'Trains telemetry loaded');

  // 2. Offline IndexedDB Event Buffering
  console.log('\nTesting 2: Offline IndexedDB Event Store & Buffering');
  const testEventId = `evt-test-offline-${Date.now()}`;
  await storeOfflineEvent(testEventId, 'ALERT_ACKNOWLEDGED', {
    alertId: 'ALT-1001',
    workerId: 'WRK-101',
    acknowledgedBy: 'Worker',
  });

  const pending = await getPendingOfflineEvents();
  assert(pending.length >= 1, 'Offline event saved to IndexedDB buffer with status PENDING');
  assert(pending.some((e) => e.eventId === testEventId), 'Buffered event matches test event ID');

  // Cleanup test item
  await offlineDb.events.where('eventId').equals(testEventId).delete();

  console.log('\n======================================================');
  console.log('🎉 Application Foundation integration tests passed.');
  console.log('======================================================\n');
}

runIntegrationSuite().catch((err) => {
  console.error('Integration test exception:', err);
  process.exit(1);
});
