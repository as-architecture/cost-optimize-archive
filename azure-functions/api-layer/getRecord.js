const cutoff = 90 * 24 * 60 * 60 * 1000;

async function getRecord(id, ts) {
  const now = new Date();
  const isHot = new Date(ts) >= new Date(now - cutoff);
  if (isHot) {
    return await hotCosmos.read(id);
  } else {
    const row = await synapse.query(`
      SELECT * FROM OPENROWSET(
        BULK 'https://yourstorage.blob.core.windows.net/coldblobs/archive/*.parquet',
        FORMAT='PARQUET'
      ) WHERE id = '${id}'
    `);
    return row;
  }
}
