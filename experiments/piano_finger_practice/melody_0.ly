\version "2.22" 
\include "lilypond-book-preamble.ly"
    
color = #(define-music-function (parser location color) (string?) #{
        \once \override NoteHead #'color = #(x11-color color)
        \once \override Stem #'color = #(x11-color color)
        \once \override Rest #'color = #(x11-color color)
        \once \override Beam #'color = #(x11-color color)
     #})
    
\header { } 
\score  { 
 \new Voice { \new Voice { \clef "treble" 
                \time 4/4
                c'' 4  
                cis'' 4  
                e'' 4  
                f'' 4  
                fis' 4  
                a' 4  
                ais' 4  
                r 16  
                b' 4  
                a' 4  
                gis' 4  
                fis' 4  
                dis'' 2  
                c'' 4  
                cis'' 4  
                dis'' 4  
                f' 4  
                g' 4  
                gis' 4  
                ais' 4  
                c'' 4  
                b' 4  
                a' 4  
                gis' 4  
                fis' 4  
                e'' 4  
                dis'' 4  
                c'' 2  
                 } 
               
 
           } 
         
 
  } 
 
\paper { }
\layout {
  \context {
    \RemoveEmptyStaffContext
    \override VerticalAxisGroup #'remove-first = ##t
  }
 }
 
