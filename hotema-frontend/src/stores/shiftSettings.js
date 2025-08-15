import { defineStore } from 'pinia'
import api from '@/lib/axios'

// Parse "HH:MM:SS" → Date object
function parseTimeToDate(timeStr) {
  if (!timeStr) return null;
  if (timeStr instanceof Date) return timeStr;
  const [h, m, s] = timeStr.split(':').map(Number);
  const date = new Date();
  date.setHours(h || 0, m || 0, s || 0, 0);
  return date;
}

// Format Date → "HH:MM:SS"
function formatTime(dateObj) {
  if (!dateObj) return null;
  if (typeof dateObj === 'string' && /^\d{2}:\d{2}(:\d{2})?$/.test(dateObj)) {
    return dateObj.length === 5 ? `${dateObj}:00` : dateObj;
  }
  if (!(dateObj instanceof Date)) return null; // cegah NaN:NaN:NaN

  const h = String(dateObj.getHours()).padStart(2, '0');
  const m = String(dateObj.getMinutes()).padStart(2, '0');
  const s = String(dateObj.getSeconds()).padStart(2, '0');
  return `${h}:${m}:${s}`;
}

export const useShiftSettings = defineStore('shiftSettings', {
  state: () => ({
    shifts: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchShifts() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get('presence/shifts/lists/');
        const data = response.data;
        if (Array.isArray(data)) {
          this.shifts = data.map((s, idx) => ({
            id: s.shift_id || idx,
            name: s.shift_name,
            start: parseTimeToDate(s.shift_start),
            stop: parseTimeToDate(s.shift_stop),
          }));
        } else {
          this.shifts = [];
          this.error = 'Format data shift tidak valid';
        }
      } catch (err) {
        this.handleError(err);
        this.shifts = [];
      } finally {
        this.loading = false;
      }
    },

    async updateShift(shift) {
      this.loading = true;
      this.error = null;
      try {
        await api.put(`presence/shifts/${shift.id}/update/`, {
          shift_name: shift.name,
          shift_start: formatTime(shift.start),
          shift_stop: formatTime(shift.stop),
        });
      } catch (err) {
        this.handleError(err);
      } finally {
        this.loading = false;
      }
    },

    handleError(err) {
      if (err.response) {
        this.error = err.response.data?.error || 'Terjadi kesalahan dari server.';
      } else if (err.request) {
        this.error = 'Tidak ada respon dari server.';
      } else {
        this.error = 'Kesalahan tidak terduga: ' + err.message;
      }
    }
  }
});
