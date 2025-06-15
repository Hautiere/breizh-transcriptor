import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
})
export class AppComponent implements OnInit {

  selectedFile!: File;
  response: any;
  isLoading = false;
  lang: 'fr' | 'br' | 'en' = 'fr';
  slogan: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.setLang(this.lang);
  }

  setLang(lang: 'fr' | 'br' | 'en') {
    this.lang = lang;
    switch (lang) {
      case 'fr':
        this.slogan = "Le breton qui s’écoute… et qui s’écrit !";
        break;
      case 'br':
        this.slogan = "Gant ar brezhoneg, eus ar vouezh d’an destenn !";
        break;
      case 'en':
        this.slogan = "Breton you can hear… and read!";
        break;
    }
  }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      this.selectedFile = target.files[0];
    }
  }

  upload() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('audio_file', this.selectedFile);

    this.isLoading = true;
    this.http.post<any>('http://localhost:8000/upload/', formData)
      .subscribe({
        next: res => {
          console.log('Réponse API', res);
          this.response = res;
          this.isLoading = false;
        },
        error: err => {
          console.error('Erreur API', err);
          this.isLoading = false;
        }
      });
  }

  download(format: 'txt' | 'json') {
    if (!this.response) return;

    const content = format === 'txt'
      ? this.response.clean_text
      : JSON.stringify(this.response, null, 2);

    const type = format === 'txt' ? 'text/plain' : 'application/json';
    const blob = new Blob([content], { type });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `transcription.${format}`;
    a.click();
    window.URL.revokeObjectURL(url);
  }
}
