// eslint-disable-next-line @typescript-eslint/no-unused-vars
export interface Link {
  category: string;
  date_added: string;
  gist_created: boolean;
  gist_id?: string;
  image_url: string;
  link_id: string;
  link_title: string;
  link_type: string;
  url: string;
}

export interface GistStatus {
  is_done_playing: boolean;
  is_now_playing: boolean;
  playback_time: number;
  in_productionQueue: boolean;
  production_status: string;
}

export interface GistSegment {
  segment_duration: number;
  segment_index: number;
  segment_title: string;
}

export interface Gist {
  gistId: string;
  category: string;
  date_created: string;
  image_url: string;
  is_played: boolean;
  is_published: boolean;
  link: string;
  playback_duration: number;
  publisher: string;
  ratings: number;
  segments: GistSegment[];
  status: GistStatus;
  title: string;
  users: number;
}
